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
    cfg = get_doc('config', 'global') or {"api_key": "", "idioma": "es"}
    safe = {k: v for k, v in cfg.items() if k != 'api_key'}
    safe['has_api_key'] = bool(cfg.get('api_key', ''))
    return safe

@app.post("/api/config")
async def save_config(body: dict = Body(...)):
    old = get_doc('config', 'global') or {}
    if not body.get('api_key'): body['api_key'] = old.get('api_key', '')
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

@app.post("/api/claude")
async def extract_with_claude(body: dict = Body(...)):
    cfg = get_doc('config', 'global') or {}
    api_key = cfg.get('api_key', '')
    if not api_key: return JSONResponse(content={'error': 'API Key no configurada'}, status_code=400)
    client = anthropic.Anthropic(api_key=api_key)
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=body.get('messages', [])
        )
        return {'text': response.content[0].text}
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

# --- FRONTEND ROUTES ---

@app.get("/")
async def serve_index():
    return FileResponse('index.html')

# Mount static files at root
# This handles style.css, script.js, etc.
app.mount("/", StaticFiles(directory=".", html=True), name="static")
