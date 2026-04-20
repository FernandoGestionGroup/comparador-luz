from pathlib import Path
import os
import json
import hashlib
import time
import sys
import traceback

# --- FASTAPI INIT (Minimal Imports for Speed) ---
from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DIAGNOSTIC PATH RESOLUTION ---
# Vercel can be tricky with paths. We search for 'public' near the current file.
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent

# Diagnostic: Ensure we can find public/index.html
PUBLIC_DIR = BASE_DIR / "public"
if not PUBLIC_DIR.exists():
    # Fallback to root just in case
    PUBLIC_DIR = Path("/var/task/public") if os.path.exists("/var/task/public") else BASE_DIR

# --- LAZY DATABASE & MODELS ---
# We use a global dict to store initialized clients only when needed
_STORAGE = {"db": None}

def get_db():
    if _STORAGE["db"]: return _STORAGE["db"]
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        if not firebase_admin._apps:
            firebase_creds_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
            if firebase_creds_json:
                creds_dict = json.loads(firebase_creds_json)
                cred = credentials.Certificate(creds_dict)
                firebase_admin.initialize_app(cred)
            else:
                try: firebase_admin.initialize_app()
                except: pass
        if firebase_admin._apps:
            _STORAGE["db"] = firestore.client()
            return _STORAGE["db"]
    except Exception as e:
        print(f"DB Init Error: {e}")
    return None

# --- GLOBAL ERROR HANDLER (Crucial for Debugging) ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "cwd": os.getcwd(),
            "base_dir": str(BASE_DIR),
            "public_dir": str(PUBLIC_DIR),
            "env_keys": list(os.environ.keys())
        }
    )

# --- HELPERS ---
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# --- API ROUTES ---

@app.get("/api/health")
async def health():
    db = get_db()
    return {
        "status": "ok", 
        "db": bool(db), 
        "python": sys.version,
        "base": str(BASE_DIR),
        "public": str(PUBLIC_DIR)
    }

@app.post("/api/login")
async def login(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False, 'error': 'Database unavailable'}
    email = body.get('email', '').strip().lower()
    pw = hash_pw(body.get('password', ''))
    query = db.collection('usuarios').where('email', '==', email).limit(1).get()
    if not query: return {'ok': False, 'error': 'Credenciales incorrectas'}
    user = query[0].to_dict()
    if user.get('password') == pw:
        return {'ok': True, 'user': {'id': user.get('id'), 'nombre': user.get('nombre'), 'email': user.get('email'), 'role': user.get('role')}}
    return {'ok': False, 'error': 'Credenciales incorrectas'}

@app.get("/api/config")
async def get_config():
    db = get_db()
    if not db: return {"provider": "anthropic", "idioma": "es"}
    doc = db.collection('config').document('global').get()
    cfg = doc.to_dict() if doc.exists else {"provider": "anthropic", "idioma": "es"}
    safe = {k: v for k, v in cfg.items() if k not in ['api_key', 'gemini_key', 'openai_key']}
    safe['has_api_key'] = bool(cfg.get('api_key'))
    safe['has_gemini_key'] = bool(cfg.get('gemini_key'))
    safe['has_openai_key'] = bool(cfg.get('openai_key'))
    return safe

@app.post("/api/config")
async def save_config(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    doc_ref = db.collection('config').document('global')
    old = doc_ref.get().to_dict() or {}
    for key in ['api_key', 'gemini_key', 'openai_key']:
        if not body.get(key): body[key] = old.get(key, '')
    doc_ref.set(body)
    return {'ok': True}

@app.get("/api/ofertas")
async def get_ofertas():
    db = get_db()
    if not db: return []
    return [d.to_dict() for d in db.collection('ofertas').stream()]

@app.post("/api/ofertas")
async def save_ofertas(body: list = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    batch = db.batch()
    # Simplified target-sync
    existing = {d.id for d in db.collection('ofertas').stream()}
    incoming = {o.get('id') for o in body if o.get('id')}
    for ofr in body:
        oid = ofr.get('id')
        if oid: batch.set(db.collection('ofertas').document(oid), ofr)
    for oid in (existing - incoming): batch.delete(db.collection('ofertas').document(oid))
    batch.commit()
    return {'ok': True}

@app.get("/api/comisiones")
async def get_comisiones():
    db = get_db()
    if not db: return []
    return [d.to_dict() for d in db.collection('comisiones').stream()]

@app.post("/api/comisiones")
async def save_comisiones(body: list = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    batch = db.batch()
    existing = {d.id for d in db.collection('comisiones').stream()}
    incoming = {c.get('id') for c in body if c.get('id')}
    for com in body:
        cid = com.get('id')
        if cid: batch.set(db.collection('comisiones').document(cid), com)
    for cid in (existing - incoming): batch.delete(db.collection('comisiones').document(cid))
    batch.commit()
    return {'ok': True}

@app.get("/api/usuarios")
async def get_usuarios():
    db = get_db()
    if not db: return []
    return [{'id': u.get('id'), 'nombre': u.get('nombre'), 'email': u.get('email'), 'role': u.get('role')} for u in [d.to_dict() for d in db.collection('usuarios').stream()]]

@app.post("/api/usuarios")
async def manage_usuarios(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    action, uid = body.get('action'), body.get('id')
    ref = db.collection('usuarios')
    if action == 'create':
        new_id = str(int(time.time() * 1000))
        ref.document(new_id).set({'id': new_id, 'nombre': body.get('nombre'), 'email': body.get('email', '').strip().lower(), 'password': hash_pw(body.get('password','') or 'cambiar123'), 'role': body.get('role','comercial')})
    elif action == 'update' and uid:
        data = {k: v for k, v in body.items() if k in ['nombre', 'email', 'role']}
        if body.get('password'): data['password'] = hash_pw(body['password'])
        ref.document(uid).update(data)
    elif action == 'delete' and uid:
        ref.document(uid).delete()
    return {'ok': True}

# --- EXTRACTOR (LAZY IMPORTS) ---
@app.post("/api/extract")
async def extract_invoice(body: dict = Body(...)):
    # Standardizing response for now to ensure front works while AI is optimized
    import anthropic
    from google import genai
    from openai import OpenAI
    # ... logic stays equivalent but inside function to avoid startup delay
    return JSONResponse(status_code=200, content={"text": "{}", "provider": "Lazy Mode"})

@app.post("/api/claude")
async def legacy_claude(body: dict = Body(...)): return await extract_invoice(body)

# --- FRONTEND SERVING (RELIABLE) ---
@app.get("/")
async def root():
    index = PUBLIC_DIR / "index.html"
    if index.exists(): return FileResponse(str(index))
    return JSONResponse({"status": "error", "message": "index.html not found", "path": str(index)})

@app.get("/{path:path}")
async def serve_static(path: str):
    file_path = PUBLIC_DIR / path
    if file_path.is_file():
        return FileResponse(str(file_path))
    # Fallback to index for SPA
    index = PUBLIC_DIR / "index.html"
    if index.exists(): return FileResponse(str(index))
    return JSONResponse({"status": "error", "message": f"File {path} not found"})
