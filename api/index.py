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
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
STATIC_DIR = PROJECT_ROOT / "public"

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
    
    # 🤖 AI HUB - ORQUESTADOR INTELIGENTE
    messages = body.get("messages", [])
    provider_manual = cfg.get("provider", "auto")
    
    # 1. Detectar tipo de archivo
    has_pdf = False
    for m in messages:
        c_list = m.get('content', [])
        if isinstance(c_list, list):
            for c in c_list:
                m_type = c.get('source', {}).get('media_type', '')
                if c.get('type') == 'document' or m_type == 'application/pdf':
                    has_pdf = True
                    break
        if has_pdf: break

    # 2. Mapeo de llaves disponibles
    keys = {
        "google": cfg.get("gemini_key"),
        "groq": cfg.get("openai_key") if (cfg.get("openai_url") and "groq" in cfg.get("openai_url")) else (cfg.get("openai_key") if cfg.get("provider")=="groq" else None),
        "openai": cfg.get("openai_key"),
        "anthropic": cfg.get("api_key")
    }
    # Fix manual para Groq por URL
    if not keys["groq"] and cfg.get("openai_url") and "groq" in cfg.get("openai_url"): keys["groq"] = cfg.get("openai_key")

    # 3. Decidir Proveedor Óptimo (Con Overwrite para PDF)
    selected = provider_manual
    
    # 🚨 REGLA DE ORO: Si hay PDF y tenemos Google, USA GOOGLE.
    if has_pdf and keys["google"]:
        selected = "google"
        print("Smart Selector: PDF DETECTADO -> Forzando Google Gemini para evitar errores")
    elif selected == "auto" or not selected:
        if has_pdf:
            selected = "google" if keys["google"] else ("anthropic" if keys["anthropic"] else "openai")
        else:
            selected = "groq" if keys["groq"] else ("openai" if keys["openai"] else ("google" if keys["google"] else "anthropic"))

    # 4. Fallback de seguridad (si el seleccionado no tiene llave)
    if not keys.get(selected) and selected != "auto":
        for p, k in keys.items():
            if k: 
                selected = p
                break

    provider = selected
    print(f"AI Hub: Ejecutando extracción vía {provider.upper()} (Manual: {provider_manual})")

    # MASTER SYSTEM PROMPT - SPANISH ENERGY EXPERT (STRICT REALITY ONLY)
    system_prompt = (
        "Eres un experto extractor de facturas eléctricas españolas (mercado libre y regulado). Tu precisión debe ser del 100%.\n\n"
        "REGLAS CRÍTICAS:\n"
        "1. IDENTIFICACIÓN DE TARIFA: Busca 'Tarifa de acceso', 'Peaje' o similar. Debe ser 2.0TD, 3.0TD o 6.1TD. Es vital para el resto de la extracción.\n"
        "2. MAPEO DE PERIODOS:\n"
        "   - Si es 2.0TD: Busca P1 (Punta), P2 (Llano) y P3 (Valle). Ignora P4-P6.\n"
        "   - Si es 3.0TD o 6.1TD: Busca los 6 periodos (P1, P2, P3, P4, P5, P6) tanto en potencia como en energía.\n"
        "3. DATOS DE POTENCIA: Extrae los kW contratados e importe para cada periodo disponible.\n"
        "4. DATOS DE ENERGÍA: Extrae los kWh consumidos y el precio unitario (€/kWh) para cada periodo.\n"
        "5. CAMPOS CLAVE: CUPS (empieza por ES...), Nombre del cliente, Dirección, CIF, Comercializadora, Total Factura, Fecha inicio/fin, IEE e IVA.\n"
        "6. PROHIBIDO INVENTAR: Si un dato no está, devuelve \"\" o 0. No uses datos de ejemplo.\n\n"
        "ESTRUCTURA DE SALIDA (Solo JSON plano):\n"
        "{\n"
        "  \"cliente\": \"\", \"cups\": \"\", \"comercializadora\": \"\", \"direccion\": \"\", \"cp\": \"\", \"tarifa\": \"\", \n"
        "  \"potencia_kw\": 0, \"dias\": 0, \"fecha_inicio\": \"YYYY-MM-DD\", \"total_factura\": 0, \n"
        "  \"iva_pct\": 21, \"iee_pct\": 5.1126963, \"iee_act\": 0, \"iva_act\": 0,\n"
        "  \"potencia\": [{\"per\":\"P1\",\"kw\":0,\"importe\":0}],\n"
        "  \"energia\": [{\"per\":\"P1\",\"kwh\":0,\"precio\":0}],\n"
        "  \"lecturas_energia\": [{\"per\":\"P1\",\"kwh\":0}],\n"
        "  \"extras_iee\": [{\"nombre\":\"Regularización FNEE\",\"importe\":0}]\n"
        "}"
    )

    try:
        # 🤖 AI HUB - ORQUESTADOR CON RETRY AUTOMÁTICO
        import re
        text = ""
        attempted_providers = []
        
        # Lista de prioridades según tipo de archivo
        if has_pdf:
            priority = ["google", "anthropic", "openai"]
        else:
            priority = ["groq", "openai", "google", "anthropic"]
        
        # Si hay una selección manual, la ponemos al principio de la prioridad
        if provider_manual != "auto" and provider_manual in priority:
            priority.remove(provider_manual)
            priority.insert(0, provider_manual)

        for provider in priority:
            if not keys.get(provider): continue
            attempted_providers.append(provider)
            print(f"AI Hub: Intentando extracción vía {provider.upper()}...")
            
            try:
                if provider == "anthropic":
                    import anthropic
                    client = anthropic.Anthropic(api_key=keys["anthropic"])
                    response = client.messages.create(
                        model=cfg.get("model") or "claude-3-5-sonnet-latest",
                        max_tokens=4096, system=system_prompt, messages=messages
                    )
                    text = response.content[0].text
                    
                elif provider == "google":
                    from google import genai
                    from google.genai import types
                    client = genai.Client(api_key=keys["google"])
                    contents = []
                    for m in messages:
                        parts = []
                        for c in m['content']:
                            if c['type'] == 'text': parts.append(types.Part.from_text(text=c['text']))
                            elif c['type'] in ['image', 'document']:
                                parts.append(types.Part.from_bytes(data=c['source']['data'], mime_type=c['source']['media_type']))
                        contents.append(types.Content(role="user" if m['role']=="user" else "model", parts=parts))
                    
                    response = client.models.generate_content(
                        model=cfg.get("model") or "gemini-2.0-flash",
                        contents=contents, config=types.GenerateContentConfig(system_instruction=system_prompt)
                    )
                    text = response.text

                elif provider in ["openai", "groq"]:
                    from openai import OpenAI
                    is_groq = (provider == "groq")
                    b_url = cfg.get("openai_url") or ("https://api.groq.com/openai/v1" if is_groq else "https://api.openai.com/v1")
                    client = OpenAI(api_key=keys["openai"], base_url=b_url)
                    
                    oa_messages = [{"role": "system", "content": system_prompt}]
                    for m in messages:
                        content = []
                        for c in m['content']:
                            if c['type'] == 'text': content.append({"type": "text", "text": c['text']})
                            elif c['type'] == 'image':
                                content.append({"type": "image_url", "image_url": {"url": f"data:{c['source']['media_type']};base64,{c['source']['data']}"}})
                        oa_messages.append({"role": m['role'], "content": content})
                    
                    default_model = "meta-llama/llama-4-scout-17b-16e-instruct" if is_groq else "gpt-4o-mini"
                    response = client.chat.completions.create(
                        model=cfg.get("model") or default_model,
                        messages=oa_messages, max_tokens=4096,
                        response_format={"type": "json_object"} if not is_groq else None 
                    )
                    text = response.choices[0].message.content

                # Si llegamos aquí sin excepción, buscamos el JSON y salimos del loop
                match = re.search(r'(\{.*\})', text, re.DOTALL)
                if match:
                    text = match.group(1)
                    return JSONResponse(status_code=200, content={"text": text, "provider": provider})
                
            except Exception as e:
                err_str = str(e)
                print(f"Error con {provider}: {err_str}")
                # Si está saturado (429) o la llave es mala (401), saltamos al siguiente
                if any(x in err_str for x in ["429", "limit", "401", "key", "authentication"]):
                    print(f"AI Hub: {provider} falló ({err_str}), saltando al siguiente...")
                    continue
                # Si es otro error desconocido, lo lanzamos
                return JSONResponse(status_code=500, content={"error": err_str, "traceback": traceback.format_exc()})

        return JSONResponse(status_code=500, content={"error": f"Todas las IAs fallaron o están saturadas. Intentado con: {attempted_providers}"})

    except Exception as e:
        err_str = str(e)
        if "429" in err_str:
            return JSONResponse(status_code=429, content={"error": "Límite de peticiones alcanzado. Espera un minuto o usa GROQ con una foto."})
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
