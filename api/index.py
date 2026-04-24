from pathlib import Path
import os
import json
import hashlib
import time
import sys
import traceback

# --- FASTAPI INIT ---
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

# --- PATH RESOLUTION (Vercel-Safe) ---
# We use 'static' instead of 'public' to avoid Vercel automatic caching/ignoring
CURRENT_DIR = Path(__file__).resolve().parent
STATIC_DIR = CURRENT_DIR / "static"

# --- LAZY DATABASE & MODELS ---
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

# --- GLOBAL ERROR HANDLER ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "cwd": os.getcwd(),
            "static_path": str(STATIC_DIR),
            "exists": STATIC_DIR.exists(),
            "dir_contents": os.listdir(str(CURRENT_DIR)) if CURRENT_DIR.exists() else []
        }
    )

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# --- API ROUTES ---

@app.get("/api/health")
async def health():
    db_ok = False
    try: db_ok = bool(get_db())
    except: pass
    return {
        "status": "ok", 
        "db": db_ok, 
        "static_exists": STATIC_DIR.exists(),
        "files": os.listdir(str(STATIC_DIR)) if STATIC_DIR.exists() else []
    }

@app.post("/api/login")
async def login(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False, 'error': 'DB Error'}
    email = body.get('email', '').strip().lower()
    pw = hash_pw(body.get('password', ''))
    q = db.collection('usuarios').where('email', '==', email).limit(1).get()
    if not q: return {'ok': False, 'error': 'Credenciales incorrectas'}
    u = q[0].to_dict()
    if u.get('password') == pw:
        return {'ok': True, 'user': {'id': u['id'], 'nombre': u['nombre'], 'email': u['email'], 'role': u['role']}}
    return {'ok': False, 'error': 'Credenciales incorrectas'}

@app.get("/api/config")
async def get_config():
    db = get_db()
    if not db: return {"provider": "anthropic"}
    d = db.collection('config').document('global').get()
    cfg = d.to_dict() if d.exists else {}
    safe = {k: v for k, v in cfg.items() if k not in ['api_key', 'gemini_key', 'openai_key']}
    for k in ['api_key', 'gemini_key', 'openai_key']: safe[f'has_{k}'] = bool(cfg.get(k))
    return safe

@app.post("/api/config")
async def save_config(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    ref = db.collection('config').document('global')
    old = ref.get().to_dict() or {}
    for k in ['api_key', 'gemini_key', 'openai_key']:
        if not body.get(k): body[k] = old.get(k, '')
    ref.set(body)
    return {'ok': True}

@app.get("/api/ofertas")
async def get_ofertas():
    db = get_db()
    return [d.to_dict() for d in db.collection('ofertas').stream()] if db else []

@app.post("/api/ofertas")
async def save_ofertas(body: list = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    batch = db.batch()
    exist = {d.id for d in db.collection('ofertas').stream()}
    incom = {o.get('id') for o in body if o.get('id')}
    for o in body:
        if o.get('id'): batch.set(db.collection('ofertas').document(o['id']), o)
    for oid in (exist - incom): batch.delete(db.collection('ofertas').document(oid))
    batch.commit()
    return {'ok': True}

@app.get("/api/comisiones")
async def get_comisiones():
    db = get_db()
    return [d.to_dict() for d in db.collection('comisiones').stream()] if db else []

@app.post("/api/comisiones")
async def save_comisiones(body: list = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    batch = db.batch()
    exist = {d.id for d in db.collection('comisiones').stream()}
    incom = {c.get('id') for c in body if c.get('id')}
    for c in body:
        if c.get('id'): batch.set(db.collection('comisiones').document(c['id']), c)
    for cid in (exist - incom): batch.delete(db.collection('comisiones').document(cid))
    batch.commit()
    return {'ok': True}

@app.get("/api/usuarios")
async def get_usuarios():
    db = get_db()
    if not db: return []
    return [{'id': u['id'], 'nombre': u['nombre'], 'email': u['email'], 'role': u['role']} for u in [d.to_dict() for d in db.collection('usuarios').stream()]]

@app.post("/api/usuarios")
async def manage_usuarios(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    action, uid = body.get('action'), body.get('id')
    ref = db.collection('usuarios')
    if action == 'create':
        nid = str(int(time.time() * 1000))
        ref.document(nid).set({'id': nid, 'nombre': body.get('nombre'), 'email': body.get('email', '').strip().lower(), 'password': hash_pw(body.get('password','') or 'cambiar123'), 'role': body.get('role','comercial')})
    elif action == 'update' and uid:
        d = {k: v for k, v in body.items() if k in ['nombre', 'email', 'role']}
        if body.get('password'): d['password'] = hash_pw(body['password'])
        ref.document(uid).update(d)
    elif action == 'delete' and uid:
        ref.document(uid).delete()
    return {'ok': True}

@app.post("/api/extract")
async def extract_invoice(body: dict = Body(...)):
    db = get_db()
    if not db: return JSONResponse(status_code=500, content={"error": "Database not initialized"})
    
    d = db.collection('config').document('global').get()
    cfg = d.to_dict() if d.exists else {}
    
    provider = cfg.get("provider", "anthropic")
    messages = body.get("messages", [])
    
    # SYSTEM PROMPT RESTRUCTURED FOR BETTER FREE MODEL PERFORMANCE
    system_prompt = (
        "Eres un experto en facturas eléctricas españolas. Tu objetivo es extraer datos técnicos con precisión quirúrgica. "
        "REGLA DE ORO: Responde únicamente con un objeto JSON plano, sin explicaciones ni bloques de código markdown.\n"
        "Estructura esperada:\n"
        "{\n"
        "  \"cliente\": \"Nombre completo\",\n"
        "  \"cups\": \"ES00...\",\n"
        "  \"comercializadora\": \"Nombre empresa\",\n"
        "  \"tarifa\": \"2.0TD | 3.0TD | 6.1TD\",\n"
        "  \"potencia_kw\": 0.00,\n"
        "  \"dias\": 0,\n"
        "  \"total_factura\": 0.00,\n"
        "  \"potencia\": [{\"per\":\"P1\",\"kw\":0,\"importe\":0}],\n"
        "  \"energia\": [{\"per\":\"P1\",\"kwh\":0,\"precio\":0}],\n"
        "  \"lecturas_energia\": [{\"per\":\"P1\",\"kwh\":0}]\n"
        "}\n"
        "Si no encuentras un dato, usa 0 o \"\". No inventes datos."
    )

    try:
        if provider == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=cfg.get("api_key"))
            response = client.messages.create(
                model=cfg.get("model") or "claude-3-5-sonnet-latest",
                max_tokens=4096,
                system=system_prompt,
                messages=messages
            )
            text = response.content[0].text
            
        elif provider == "google":
            from google import genai
            from google.genai import types
            key = cfg.get("gemini_key")
            if not key: return JSONResponse(status_code=400, content={"error": "Falta la API Key de Google"})
            client = genai.Client(api_key=key)
            
            contents = []
            for m in messages:
                parts = []
                for c in m['content']:
                    if c['type'] == 'text':
                        parts.append(types.Part.from_text(text=c['text']))
                    elif c['type'] in ['image', 'document']:
                        parts.append(types.Part.from_bytes(data=c['source']['data'], mime_type=c['source']['media_type']))
                contents.append(types.Content(role="user" if m['role']=="user" else "model", parts=parts))
            
            response = client.models.generate_content(
                model=cfg.get("model") or "gemini-2.0-flash",
                contents=contents,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            text = response.text

        elif provider in ["openai", "groq"]:
            from openai import OpenAI
            is_groq = (provider == "groq")
            b_url = cfg.get("openai_url") or ("https://api.groq.com/openai/v1" if is_groq else "https://api.openai.com/v1")
            api_key = cfg.get("openai_key")
            
            if not api_key: return JSONResponse(status_code=400, content={"error": f"Falta la API Key para {provider.upper()}"})
            
            client = OpenAI(api_key=api_key, base_url=b_url)
            
            # Message adaptation for Vision-capable models
            oa_messages = [{"role": "system", "content": system_prompt}]
            for m in messages:
                content = []
                for c in m['content']:
                    if c['type'] == 'text':
                        content.append({"type": "text", "text": c['text']})
                    elif c['type'] == 'image':
                        content.append({"type": "image_url", "image_url": {"url": f"data:{c['source']['media_type']};base64,{c['source']['data']}"}})
                oa_messages.append({"role": m['role'], "content": content})
            
            default_model = "llama-3.2-90b-vision-preview" if is_groq else "gpt-4o"
            response = client.chat.completions.create(
                model=cfg.get("model") or default_model,
                messages=oa_messages,
                max_tokens=4096,
                response_format={"type": "json_object"} if not is_groq else None 
            )
            text = response.choices[0].message.content
        else:
            return JSONResponse(status_code=400, content={"error": f"Proveedor no soportado: {provider}"})

        return JSONResponse(status_code=200, content={"text": text, "provider": provider})

    except Exception as e:
        err_str = str(e)
        if "429" in err_str:
            return JSONResponse(status_code=429, content={"error": "Límite de peticiones alcanzado. Espera un minuto o cambia a GROQ (gratis y rápido)."})
        return JSONResponse(status_code=500, content={"error": err_str, "traceback": traceback.format_exc()})

@app.post("/api/claude")
async def legacy_claude(body: dict = Body(...)): return await extract_invoice(body)

# --- SERVING FRONTEND ---
@app.get("/")
async def serve_root():
    index = STATIC_DIR / "index.html"
    if index.exists(): return FileResponse(str(index))
    return JSONResponse({"error": "index.html not found", "path": str(index), "cwd": os.getcwd()})

@app.get("/{path:path}")
async def serve_static(path: str):
    if path.startswith("api/"): return JSONResponse({"error": "Route not found"}, status_code=404)
    file = STATIC_DIR / path
    if file.is_file(): return FileResponse(str(file))
    index = STATIC_DIR / "index.html"
    if index.exists(): return FileResponse(str(index))
    return JSONResponse({"error": f"File {path} not found", "tried": str(file)})
