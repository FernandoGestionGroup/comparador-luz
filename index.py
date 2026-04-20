from pathlib import Path
import os
import json
import hashlib
import time

# --- FASTAPI INIT ---
from fastapi import FastAPI, Body, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

# --- LAZY/SAFE IMPORTS & FIREBASE ---
db = None
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    import anthropic
    from google import genai
    from openai import OpenAI

    # Initialize Firebase
    if not firebase_admin._apps:
        firebase_creds_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
        if firebase_creds_json:
            try:
                creds_dict = json.loads(firebase_creds_json)
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                print(f"Firebase JSON Error: {e}")
                try: firebase_admin.initialize_app()
                except: pass
        else:
            try: firebase_admin.initialize_app()
            except: pass
    
    if firebase_admin._apps:
        db = firestore.client()
except Exception as e:
    print(f"Startup/Import Error: {e}")

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
    if not db: return {'ok': False, 'error': 'Database not initialized'}
    email = body.get('email', '').strip().lower()
    pw = hash_pw(body.get('password', ''))
    
    # Selective query: Much faster and cheaper than get_collection
    try:
        query = db.collection('usuarios').where('email', '==', email).limit(1).get()
        if not query:
            return {'ok': False, 'error': 'Credenciales incorrectas'}
        
        user = query[0].to_dict()
        if user.get('password') == pw:
            return {
                'ok': True, 
                'user': {
                    'id': user.get('id'), 
                    'nombre': user.get('nombre'), 
                    'email': user.get('email'), 
                    'role': user.get('role')
                }
            }
    except Exception as e:
        print(f"Login error: {e}")
        return {'ok': False, 'error': 'Internal server error'}
        
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
async def get_ofertas(): 
    return get_collection('ofertas')

@app.post("/api/ofertas")
async def save_ofertas(body: List[dict] = Body(...)):
    if not db: return {'ok': False, 'error': 'Database not initialized'}
    
    # Incremental update logic: 
    # 1. Get existing IDs
    existing_docs = db.collection('ofertas').stream()
    existing_ids = {doc.id for doc in existing_docs}
    incoming_ids = {o.get('id') for o in body if o.get('id')}
    
    batch = db.batch()
    # 2. Update or Create
    for ofr in body:
        oid = ofr.get('id')
        if not oid: continue
        batch.set(db.collection('ofertas').document(oid), ofr)
    
    # 3. Targeted Delete (orphans)
    to_delete = existing_ids - incoming_ids
    for oid in to_delete:
        batch.delete(db.collection('ofertas').document(oid))
    
    batch.commit()
    return {'ok': True}

@app.get("/api/comisiones")
async def get_comisiones(): 
    return get_collection('comisiones')

@app.post("/api/comisiones")
async def save_comisiones(body: List[dict] = Body(...)):
    if not db: return {'ok': False, 'error': 'Database not initialized'}
    
    existing_docs = db.collection('comisiones').stream()
    existing_ids = {doc.id for doc in existing_docs}
    incoming_ids = {c.get('id') for c in body if c.get('id')}
    
    batch = db.batch()
    for com in body:
        cid = com.get('id')
        if not cid: continue
        batch.set(db.collection('comisiones').document(cid), com)
    
    # Targeted delete for commissions no longer in the list
    to_delete_coms = existing_ids - incoming_ids
    for cid in to_delete_coms:
        batch.delete(db.collection('comisiones').document(cid))
        
    batch.commit()
    return {'ok': True}

@app.get("/api/usuarios")
async def get_usuarios():
    users = get_collection('usuarios')
    return [{'id': u.get('id'), 'nombre': u.get('nombre'), 'email': u.get('email'), 'role': u.get('role')} for u in users]

@app.post("/api/usuarios")
async def manage_usuarios(body: dict = Body(...)):
    if not db: return {'ok': False, 'error': 'Database not initialized'}
    action = body.get('action')
    users_ref = db.collection('usuarios')
    
    if action == 'create':
        email = body.get('email', '').strip().lower()
        existing = users_ref.where('email', '==', email).limit(1).get()
        if existing:
            return {'ok': False, 'error': 'El email ya existe'}
            
        new_id = str(int(time.time() * 1000))
        pw = hash_pw(body.get('password', '')) if body.get('password') else hash_pw('cambiar123')
        user_data = {
            'id': new_id,
            'nombre': body.get('nombre'),
            'email': email,
            'password': pw,
            'role': body.get('role', 'comercial')
        }
        users_ref.document(new_id).set(user_data)
        
    elif action == 'update':
        uid = body.get('id')
        if not uid: return {'ok': False, 'error': 'Missing ID'}
        doc_ref = users_ref.document(uid)
        update_data = {
            'nombre': body.get('nombre'),
            'email': body.get('email', '').strip().lower(),
            'role': body.get('role')
        }
        if body.get('password'):
            update_data['password'] = hash_pw(body['password'])
        doc_ref.update({k: v for k, v in update_data.items() if v is not None})
        
    elif action == 'delete':
        uid = body.get('id')
        if not uid: return {'ok': False, 'error': 'Missing ID'}
        users_ref.document(uid).delete()
        
    return {'ok': True}

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
    discovered_names = []
    
    for version in ['v1', 'v1beta']:
        try:
            client = genai.Client(api_key=key, http_options={'api_version': version})
            
            # Step 1: Discover all models once and store names
            if not discovered_names:
                try:
                    for m in client.models.list():
                        if 'generateContent' in getattr(m, 'supported_generation_methods', []):
                            discovered_names.append(m.name)
                except: pass

            # Step 2: Try recommended models with and without 'models/' prefix
            current_queue = []
            for m in models_to_try:
                if not m: continue
                current_queue.append(m.replace('models/', ''))
                current_queue.append(f"models/{m.replace('models/', '')}")
            
            # Add discovered models to the end
            for d in discovered_names:
                if d not in current_queue: current_queue.append(d)

            for m_id in current_queue:
                try:
                    res = client.models.generate_content(model=m_id, contents=contents)
                    return {'text': res.text, 'model': f"{m_id} ({version})", 'provider': 'Google'}, None
                except Exception as e:
                    last_err = str(e)
                    # Continue loop to next model/version
        except Exception as ve:
            last_err = f"Client init error ({version}): {str(ve)}"
            
    diag = f"[Diagnóstico Google] Modelos: {', '.join(discovered_names) or 'Ninguno'}. Llave probada: {key[:4]}..."
    return None, f"Google: {last_err}. {diag}"

def try_openai(cfg, model_name, messages, provider='openai'):
    key = cfg.get('openai_key', '')
    base_url = cfg.get('openai_url', 'https://api.openai.com/v1')
    if provider == 'groq' and 'groq' not in base_url: base_url = 'https://api.groq.com/openai/v1'
    if not key: return None, "Key missing"
    
    # OpenRouter specific headers for better service
    extra_headers = {
        "HTTP-Referer": "https://comparador-luz.vercel.app",
        "X-Title": "Comparador Luz B2B"
    }

    client = OpenAI(api_key=key, base_url=base_url, default_headers=extra_headers)
    oa_messages = []
    for msg in messages:
        oa_content = []
        for content in msg.get('content', []):
            if content['type'] == 'text':
                oa_content.append({"type": "text", "text": content['text']})
            elif content['type'] == 'image' or content['type'] == 'document':
                src = content.get('source', {})
                data = src.get('data', '')
                mtype = src.get('media_type', 'image/jpeg')
                # OpenAI standard for vision
                oa_content.append({"type": "image_url", "image_url": {"url": f"data:{mtype};base64,{data}"}})
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

def smart_dispatch(key):
    """Identifies provider and configures defaults based on key prefix."""
    if not key: return None
    key = key.strip()
    
    if key.startswith('sk-or-'):
        return {
            'type': 'openai',
            'url': 'https://openrouter.ai/api/v1',
            # List of reliable Vision models for April 2026
            'models': [
                'openrouter/free', # AUTO-ROUTING to current free models (No credits needed)
                'google/gemini-2.0-flash-001',
                'meta-llama/llama-3.2-11b-vision-instruct:free'
            ],
            'name': 'OpenRouter'
        }
    elif key.startswith('AIza'):
        return {
            'type': 'google',
            'model': 'gemini-2.0-flash',
            'name': 'Google Gemini'
        }
    elif key.startswith('sk-ant-'):
        return {
            'type': 'anthropic',
            'model': 'claude-3-5-sonnet-latest',
            'name': 'Anthropic'
        }
    elif key.startswith('sk-'):
        return {
            'type': 'openai',
            'url': 'https://api.openai.com/v1',
            'model': 'gpt-4o-mini',
            'name': 'OpenAI'
        }
    return None

@app.post("/api/extract")
async def extract_invoice(body: dict = Body(...)):
    cfg = get_doc('config', 'global') or {}
    messages = body.get('messages', [])
    
    # 1. Gather all potential keys
    potential_keys = [
        cfg.get('openai_key', ''),
        cfg.get('api_key', ''), # Anthropic
        cfg.get('gemini_key', '')
    ]
    
    # Context prepared for Gemini
    gemini_contents = []
    for msg in messages:
        for cnt in msg.get('content', []):
            if cnt['type'] == 'text': gemini_contents.append(cnt['text'])
            elif cnt['type'] in ['image', 'document']:
                src = cnt.get('source', {})
                gemini_contents.append(genai.types.Part.from_bytes(data=src.get('data', ''), mime_type=src.get('media_type', 'application/pdf')))

    errors = []
    tried_keys = set()

    for key in potential_keys:
        if not key or key in tried_keys: continue
        tried_keys.add(key)
        
        info = smart_dispatch(key)
        if not info: continue
        
        # Prepare model list (Priority: 1. User specified, 2. Smart Defaults)
        user_model = cfg.get('model', '').strip()
        models_to_try = [user_model] if user_model else info.get('models', [info.get('model')])
        
        for model_to_use in models_to_try:
            if not model_to_use: continue
            res, err = None, None
            if info['type'] == 'google':
                res, err = try_google(cfg, model_to_use, gemini_contents, [model_to_use])
            elif info['type'] == 'anthropic':
                tmp_cfg = cfg.copy(); tmp_cfg['api_key'] = key
                res, err = try_anthropic(tmp_cfg, model_to_use, messages)
            elif info['type'] == 'openai':
                tmp_cfg = cfg.copy(); tmp_cfg['openai_key'] = key; tmp_cfg['openai_url'] = info.get('url')
                res, err = try_openai(tmp_cfg, model_to_use, messages, info['name'].lower())
                
            if res:
                res['provider'] = info['name']
                return res
            
            # If model literal fail (404), continue to next model in list
            if err:
                last_err = f"{info['name']} ({model_to_use}): {err}"
                errors.append(last_err)

    return JSONResponse(content={'error': " | ".join(errors) or "No se detectaron llaves válidas. Revisa la Configuración."}, status_code=500)

@app.post("/api/claude")
async def legacy_claude(body: dict = Body(...)):
    # Compatibility with old frontend until updated
    return await extract_invoice(body)

# --- FRONTEND ROUTES ---

@app.get("/")
async def serve_root():
    return FileResponse(str(BASE_DIR / "public" / "index.html"))

# Mount static files (only if dir exists)
public_path = BASE_DIR / "public"
if public_path.exists():
    app.mount("/public", StaticFiles(directory=str(public_path)), name="public")

@app.get("/{file_path:path}")
async def serve_static_files(file_path: str):
    # Security: prevent path traversal if any
    safe_path = (public_path / file_path).resolve()
    if not str(safe_path).startswith(str(public_path)):
        return FileResponse(str(public_path / "index.html"))

    if safe_path.is_file():
        return FileResponse(str(safe_path))
    
    # Return index.html for SPA/Unknown paths
    return FileResponse(str(public_path / "index.html"))
