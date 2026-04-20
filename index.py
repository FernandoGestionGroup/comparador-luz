import os
import json
import hashlib
import time
from typing import List
from fastapi import FastAPI, Body, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
import anthropic
import google.genai as genai
from google.genai import types
from openai import OpenAI

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
firebase_creds_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if firebase_creds_json:
    try:
        creds_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase Init Error: {e}")
else:
    try:
        firebase_admin.initialize_app()
    except:
        pass

db = firestore.client() if firebase_admin._apps else None

# --- HELPERS ---
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_doc(collection, doc_id):
    if not db: return None
    doc = db.collection(collection).document(doc_id).get()
    return doc.to_dict() if doc.exists else None

def set_doc(collection, doc_id, data):
    if not db: return
    db.collection(collection).document(doc_id).set(data)

def get_collection(collection):
    if not db: return []
    docs = db.collection(collection).stream()
    return [doc.to_dict() for doc in docs]

# --- API ROUTES ---

@app.post("/api/login")
async def login(body: dict = Body(...)):
    email = body.get('email', '').strip().lower()
    pw = hash_pw(body.get('password', ''))
    users = get_collection('usuarios')
    user = next((u for u in users if u['email'].lower() == email and u['password'] == pw), None)
    if user:
        return {'ok': True, 'user': {'id': user['id'], 'nombre': user['nombre'], 'email': user['email'], 'role': user['role']}}
    return {'ok': False, 'error': 'Credenciales incorrectas'}

@app.get("/api/config")
async def get_config():
    cfg = get_doc('config', 'global') or {"provider": "anthropic", "idioma": "es"}
    # Mask keys
    safe = {k: v for k, v in cfg.items() if k not in ['api_key', 'gemini_key', 'openai_key']}
    safe['has_api_key'] = bool(cfg.get('api_key'))
    safe['has_gemini_key'] = bool(cfg.get('gemini_key'))
    safe['has_openai_key'] = bool(cfg.get('openai_key'))
    return safe

@app.post("/api/config")
async def save_config(body: dict = Body(...)):
    old = get_doc('config', 'global') or {}
    # Preserve keys if not sent
    if not body.get('api_key'): body['api_key'] = old.get('api_key', '')
    if not body.get('gemini_key'): body['gemini_key'] = old.get('gemini_key', '')
    if not body.get('openai_key'): body['openai_key'] = old.get('openai_key', '')
    set_doc('config', 'global', body)
    return {'ok': True}

@app.get("/api/ofertas")
async def get_ofertas(): return get_collection('ofertas')

@app.get("/api/comisiones")
async def get_comisiones(): return get_collection('comisiones')

@app.get("/api/usuarios")
async def get_usuarios():
    users = get_collection('usuarios')
    return [{'id': u['id'], 'nombre': u['nombre'], 'email': u['email'], 'role': u['role']} for u in users]

RECOMMENDED_MODELS = {
    'google': ['gemini-2.0-flash', 'gemini-1.5-flash-latest', 'gemini-1.5-flash'],
    'anthropic': ['claude-3-5-sonnet-20241022', 'claude-3-5-sonnet-latest'],
    'openai': ['gpt-4o', 'gpt-4o-mini'],
    'groq': ['llama-3.3-70b-versatile', 'llama3-70b-8192']
}

def try_google(cfg, model_name, contents, models_to_try):
    key = cfg.get('gemini_key', '')
    if not key: return None, "Key missing"
    
    last_err = ""
    # Try both stable (v1) and experimental (v1beta) channels
    for version in ['v1', 'v1beta']:
        client = genai.Client(api_key=key, http_options={'api_version': version})
        
        # Try recommended models in this version
        for m in models_to_try:
            if not m: continue
            try:
                res = client.models.generate_content(model=m, contents=contents)
                return {'text': res.text, 'model': f"{m} ({version})", 'provider': 'Google'}, None
            except Exception as e:
                last_err = str(e)
                # If it's something that's NOT a model-not-found, it might be auth/quota, so return it
                if not any(x in last_err.lower() for x in ['404', 'not found']):
                    # If it's a 429 or other, we might still want to try discovery or other version
                    pass
        
        # If no models worked in this version, try discovery in this version
        try:
            for m in client.models.list():
                methods = getattr(m, 'supported_generation_methods', [])
                if 'generateContent' in methods:
                    try:
                        res = client.models.generate_content(model=m.name, contents=contents)
                        return {'text': res.text, 'model': f"{m.name} ({version})", 'provider': 'Google (Discovered)'}, None
                    except: continue
        except: pass
        
    return None, f"Gemini ({version}): {last_err}"

def try_openai(cfg, model_name, messages, provider='openai'):
    key = cfg.get('openai_key', '')
    base_url = cfg.get('openai_url', 'https://api.openai.com/v1')
    if provider == 'groq' and 'groq' not in base_url: base_url = 'https://api.groq.com/openai/v1'
    if not key: return None, "Key missing"
    
    client = OpenAI(api_key=key, base_url=base_url)
    oa_messages = []
    for msg in messages:
        oa_content = []
        for content in msg.get('content', []):
            if content['type'] == 'text':
                oa_content.append({"type": "text", "text": content['text']})
            elif content['type'] == 'image':
                src = content.get('source', {})
                oa_content.append({"type": "image_url", "image_url": {"url": f"data:{src.get('media_type')};base64,{src.get('data')}"}})
        oa_messages.append({"role": msg.get('role', 'user'), "content": oa_content})

    try:
        res = client.chat.completions.create(model=model_name, messages=oa_messages, max_tokens=2000)
        return {'text': res.choices[0].message.content, 'model': model_name, 'provider': provider.upper()}, None
    except Exception as e:
        return None, str(e)

def try_anthropic(cfg, model_name, messages):
    key = cfg.get('api_key', '')
    if not key: return None, "Key missing"
    client = anthropic.Anthropic(api_key=key)
    try:
        res = client.messages.create(model=model_name, max_tokens=2000, messages=messages)
        return {'text': res.content[0].text, 'model': model_name, 'provider': 'Anthropic'}, None
    except Exception as e:
        return None, str(e)

@app.post("/api/extract")
async def extract_invoice(body: dict = Body(...)):
    cfg = get_doc('config', 'global') or {}
    messages = body.get('messages', [])
    selected_provider = cfg.get('provider', 'anthropic')
    
    # Priority List: 1. Selected, 2. Fallbacks
    all_providers = ['google', 'anthropic', 'openai', 'groq']
    fallback_queue = [selected_provider] + [p for p in all_providers if p != selected_provider]
    
    last_overall_error = "No provider available"
    
    # Context prepared for Gemini
    gemini_contents = []
    from google.genai import types
    for msg in messages:
        for cnt in msg.get('content', []):
            if cnt['type'] == 'text': gemini_contents.append(cnt['text'])
            elif cnt['type'] in ['image', 'document']:
                src = cnt.get('source', {})
                gemini_contents.append(types.Part.from_bytes(data=src.get('data', ''), mime_type=src.get('media_type', 'application/pdf')))

    for prov in fallback_queue:
        res, err = None, None
        if prov == 'google':
            pref = cfg.get('gemini_model', '').strip()
            models = [pref] if pref else RECOMMENDED_MODELS['google']
            res, err = try_google(cfg, pref, gemini_contents, models)
        elif prov == 'anthropic':
            res, err = try_anthropic(cfg, cfg.get('anthropic_model', 'claude-3-5-sonnet-latest'), messages)
        elif prov == 'openai' or prov == 'groq':
            res, err = try_openai(cfg, cfg.get(f'{prov}_model', RECOMMENDED_MODELS[prov][0]), messages, prov)
            
        if res: return res # SUCCESS!
        if err and "Key missing" not in err:
            last_overall_error = f"{prov.upper()}: {err}"

    return JSONResponse(content={'error': f"Todos los proveedores fallaron. Último error: {last_overall_error}"}, status_code=500)

@app.post("/api/claude")
async def legacy_claude(body: dict = Body(...)):
    # Compatibility with old frontend until updated
    return await extract_invoice(body)

# --- FRONTEND ROUTES ---

@app.get("/")
async def serve_index():
    return FileResponse('index.html')

# Mount static files at root
# This handles style.css, script.js, etc.
app.mount("/", StaticFiles(directory=".", html=True), name="static")
