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

@app.post("/api/extract")
async def extract_invoice(body: dict = Body(...)):
    cfg = get_doc('config', 'global') or {}
    provider = cfg.get('provider', 'anthropic')
    messages = body.get('messages', [])
    
    # Get user preferred model or the first from our recommended list
    preferred = cfg.get('gemini_model' if provider=='google' else f'{provider}_model', '').strip()
    models_to_try = [preferred] if preferred else RECOMMENDED_MODELS.get(provider, [])
    if preferred and preferred not in RECOMMENDED_MODELS.get(provider, []):
        # Add the recommended ones as fallbacks if the user chose a specific one
        models_to_try += RECOMMENDED_MODELS.get(provider, [])

    last_error = "No models available for provider"
    
    for model_name in models_to_try:
        if not model_name: continue
        try:
            if provider == 'google':
                key = cfg.get('gemini_key', '')
                if not key: return JSONResponse(content={'error': 'Gemini API Key no configurada'}, status_code=400)
                
                # Using modern client (defaults to v1 stable in 2026 SDK)
                client = genai.Client(api_key=key, http_options={'api_version': 'v1'})
                
                # Convert messages to new format
                contents = []
                for msg in messages:
                    for cnt in msg.get('content', []):
                        if cnt['type'] == 'text':
                            contents.append(cnt['text'])
                        elif cnt['type'] == 'image' or cnt['type'] == 'document':
                            src = cnt.get('source', {})
                            contents.append(types.Part.from_bytes(
                                data=src.get('data', ''),
                                mime_type=src.get('media_type', 'application/pdf')
                            ))
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
                return {'text': response.text, 'model': model_name}

            elif provider == 'openai' or provider == 'groq':
                is_groq = (provider == 'groq')
                key = cfg.get('openai_key', '')
                base_url = cfg.get('openai_url', 'https://api.openai.com/v1')
                if is_groq and 'groq' not in base_url: base_url = 'https://api.groq.com/openai/v1'
                
                if not key: return JSONResponse(content={'error': f'{provider.upper()} API Key no configurada'}, status_code=400)
                client = OpenAI(api_key=key, base_url=base_url)
                
                oa_messages = []
                for msg in messages:
                    oa_content = []
                    for content in msg.get('content', []):
                        if content['type'] == 'text':
                            oa_content.append({"type": "text", "text": content['text']})
                        elif content['type'] == 'image':
                            src = content.get('source', {})
                            oa_content.append({
                                "type": "image_url",
                                "image_url": {"url": f"data:{src.get('media_type')};base64,{src.get('data')}"}
                            })
                    oa_messages.append({"role": msg.get('role', 'user'), "content": oa_content})

                response = client.chat.completions.create(
                    model=model_name,
                    messages=oa_messages,
                    max_tokens=2000
                )
                return {'text': response.choices[0].message.content, 'model': model_name}

            else: # anthropic
                key = cfg.get('api_key', '')
                if not key: return JSONResponse(content={'error': 'Anthropic API Key no configurada'}, status_code=400)
                client = anthropic.Anthropic(api_key=key)
                response = client.messages.create(
                    model=model_name,
                    max_tokens=2000,
                    messages=messages
                )
                return {'text': response.content[0].text, 'model': model_name}
                
        except Exception as e:
            err_str = str(e)
            last_error = err_str
            # If it's a "Not Found" (404) or "Quota/Rate Limit" (429), try next model
            # For Gemini/Google, check for specific substrings in error
            is_fallback_case = any(x in err_str.lower() for x in ['404', 'not found', '429', 'quota', 'limit'])
            if not is_fallback_case:
                # If it's a persistent error (auth, etc.), don't bother trying other models
                break
            # Otherwise, loop continues to next model
    
    return JSONResponse(content={'error': last_error}, status_code=500)

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
