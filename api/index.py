from pathlib import Path
import os
import json
import hashlib
import time
import sys
import traceback
import re

# --- FASTAPI INIT ---
from fastapi import FastAPI, Body, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

import uuid
from passlib.context import CryptContext
from firebase_admin import firestore
import anthropic
from openai import OpenAI
try: from google import genai; from google.genai import types
except: genai = None; types = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY ---
API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False)
MASTER_API_KEY = os.environ.get("MASTER_API_KEY") # Sin valor por defecto por seguridad
PASSWORD_SALT = os.environ.get("PASSWORD_SALT", "GG_STUDIO_SALT_PROTECT_2026")
SESSION_EXPIRE_SECONDS = 86400 # 24 horas

async def get_current_user(api_key: str = Depends(API_KEY_HEADER)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Unauthorized: No API Key provided")
    
    # Soporte para la Master Key (retrocompatibilidad para el admin inicial si es necesario)
    if api_key == MASTER_API_KEY:
        return {"id": "master", "role": "admin", "nombre": "Master"}

    db = get_db()
    if not db:
        raise HTTPException(status_code=500, detail="Database error")
    
    # Verificar sesión en Firestore
    session = db.collection('_sessions').document(api_key).get()
    if not session.exists:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or expired session")
    
    sdata = session.to_dict()
    
    # Validación de expiración
    created_at = sdata.get('created_at', 0)
    if time.time() - created_at > SESSION_EXPIRE_SECONDS:
        # Opcional: eliminar sesión expirada
        # db.collection('_sessions').document(api_key).delete()
        raise HTTPException(status_code=401, detail="Unauthorized: Session expired")
        
    return sdata

async def verify_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Admin access required")
    return user

# --- CONFIGURACIÓN DE RUTAS ESTÁTICAS (Nueva estructura interna) ---
STATIC_DIR = Path(__file__).resolve().parent / "static"

# Fallback para desarrollo local (si la carpeta sigue en la raíz)
if not STATIC_DIR.exists():
    STATIC_DIR = Path(__file__).resolve().parent.parent / "public"

print(f"Directorio Estático detectado: {STATIC_DIR}")

@app.get("/")
async def read_index():
    idx = STATIC_DIR / "index.html"
    if idx.exists(): return FileResponse(str(idx))
    return {"status": "ok", "msg": "Frontend no detectado", "path": str(STATIC_DIR)}

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
            db = firestore.client()
            _STORAGE["db"] = db
            
            # --- AUTO MIGRATION (Only if Firestore is empty) ---
            try:
                # 1. Config
                cfg_doc = db.collection('config').document('global').get()
                if not cfg_doc.exists and os.path.exists('config_db.json'):
                    print("Migrando Configuración local a Firebase...")
                    with open('config_db.json', 'r', encoding='utf-8') as f:
                        db.collection('config').document('global').set(json.load(f))
                
                # 2. Ofertas
                of_count = db.collection('ofertas').limit(1).get()
                if not of_count and os.path.exists('ofertas_db.json'):
                    print("Migrando Ofertas locales a Firebase...")
                    with open('ofertas_db.json', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for item in data:
                                if item.get('id'): db.collection('ofertas').document(str(item['id'])).set(item)
            except Exception as em:
                print(f"Error en auto-migración: {em}")
                
            return _STORAGE["db"]
    except Exception as e:
        print(f"DB Init Error: {e}")
    return None

# --- GLOBAL ERROR HANDLER ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Loguear el error internamente (opcionalmente a un servicio como Sentry)
    print(f"CRITICAL ERROR: {str(exc)}")
    print(traceback.format_exc())
    
    # Respuesta segura para el cliente (sin tracebacks ni rutas)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor. Por favor, contacte con soporte.",
            "type": exc.__class__.__name__
        }
    )

def hash_pw(pw):
    return pwd_context.hash(pw + PASSWORD_SALT)

def verify_pw(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw + PASSWORD_SALT, hashed_pw)

def hash_pw_legacy(pw):
    return hashlib.sha256((pw + PASSWORD_SALT).encode()).hexdigest()

def hash_pw_very_legacy(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# --- CALCULATION ENGINE ---

def calculate_comision(oferta, d, comisiones):
    pot = d.get('potencia_kw', 0)
    consumo = d.get('consumo_anual', 0)
    dias = d.get('dias', 0)
    
    def clean_str(s):
        return (s or "").lower().strip()
        
    co_name = clean_str(oferta.get('comercializadora'))
    regla = next((c for c in comisiones if clean_str(c.get('comercializadora')) == co_name), None)
    
    if regla and regla.get('tramos'):
        for t in regla['tramos']:
            try:
                match_pot = pot >= float(t.get('p_min', 0)) and pot < float(t.get('p_max', 9999))
                match_cons = consumo >= float(t.get('c_min', 0)) and consumo < float(t.get('c_max', 99999999))
                
                filtro = clean_str(t.get('filtro'))
                match_name = not filtro or filtro in clean_str(oferta.get('nombre'))
                
                if match_pot and match_cons and match_name:
                    if t.get('tipo') == 'variable':
                        return float(t.get('valor', 0)) * (consumo / 1000)
                    return float(t.get('valor', 0)) * (dias / 365)
            except: continue
                
    return float(oferta.get('comision', 0)) * (dias / 365)

def calculate_offer(d, o, comisiones):
    dias = d.get('dias', 0)
    pot_kw = d.get('potencia_kw', 0)
    sim_by_per = d.get('lec_by_per', {})
    
    periods = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']
    
    # 1. Potencia
    t_pot = 0
    for p in periods:
        pp_nva = o.get(f'pp_{p}', 0)
        if pp_nva > 0:
            t_pot += pot_kw * pp_nva * dias
            
    t_pot *= (1 - o.get('dto_potencia', 0) / 100)
    
    # 2. Energía
    t_en = 0
    dto_global = o.get('dto_energia_global', 0) / 100
    is_discriminated = o.get('dto_energia_por_periodo', False)
    
    for i, p in enumerate(periods):
        kwh = sim_by_per.get(p.upper(), 0)
        precio = o.get(f'ep_{p}', 0)
        
        dto = (o.get(f'dto_e_p{i+1}', 0) / 100) if is_discriminated else dto_global
        t_en += kwh * precio * (1 - dto)
        
    # 3. Autoconsumo
    comp_nva = 0
    if d.get('tiene_autoconsumo'):
        comp_nva = d.get('autoconsumo_kwh', 0) * o.get('compensacion', 0)
        
    # 4. Otros conceptos
    rea = d.get('reactiva', 0)
    exc = d.get('exceso_potencia', 0)
    alq = d.get('alquiler_equipos', 0)
    bon = d.get('bono_social', 0)
    
    # Extras IEE
    extras_iee = sum(e.get('importe', 0) for e in d.get('iee_extras', []) if e.get('mantiene'))
    
    # Base IEE
    base_iee = t_pot + t_en + rea + exc + bon + extras_iee - comp_nva
    iee = base_iee * (d.get('iee_pct', 5.1126963) / 100)
    
    # Extras NO IEE
    no_iee_extras = sum(e.get('importe', 0) for e in d.get('no_iee_extras', []) if e.get('mantiene'))
    
    # Base IVA
    base_iva = base_iee + iee + alq + no_iee_extras
    iva = base_iva * (d.get('iva_pct', 21) / 100)
    
    total = base_iva + iva
    comision = calculate_comision(o, d, comisiones)
    
    return {
        'id': o.get('id'),
        'nombre': o.get('nombre'),
        'comercializadora': o.get('comercializadora'),
        'tipo': o.get('tipo'),
        'permanencia': o.get('permanencia'),
        'validez': o.get('validez'),
        'total': total,
        'comision': comision,
        'tPot': t_pot,
        'tEn': t_en,
        'compNva': comp_nva,
        'iee': iee,
        'baseIEE': base_iee,
        'baseIVA': base_iva,
        'iva': iva
    }

# --- API ROUTES ---

@app.get("/api/health")
async def health():
    # Esta ruta se mantiene pública para health checks de Vercel
    db_ok = False
    try: db_ok = bool(get_db())
    except: pass
    return {
        "status": "ok", 
        "db": db_ok, 
        "static_exists": STATIC_DIR.exists()
    }

@app.post("/api/login")
async def login(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False, 'error': 'Database Connection Error'}
    email = body.get('email', '').strip().lower()
    password_plain = body.get('password', '')
    
    # --- ROBUST LOGIN & AUTO-REPAIR ---
    u = None
    # 1. Intentar búsqueda exacta
    users_ref = db.collection('usuarios').where('email', '==', email).limit(1).stream()
    for doc in users_ref:
        u = doc.to_dict()
        u['id'] = doc.id
        break
    
    # 2. Si no se encuentra, buscar en toda la colección (para evitar temas de mayúsculas)
    if not u:
        all_docs = db.collection('usuarios').stream()
        for doc in all_docs:
            udata = doc.to_dict()
            if udata.get('email', '').lower() == email:
                u = udata
                u['id'] = doc.id
                break
    
    # 3. AUTO-REPAIR: Si sigue sin aparecer Y es el admin por defecto, lo creamos/reparamos
    if not u and email == "admin@gestiongroup.es":
        print("Reparando usuario admin por defecto...")
        u = {
            "nombre": "Administrador",
            "email": "admin@gestiongroup.es",
            "password": pwd_context.hash("admin123"),
            "role": "admin"
        }
        db.collection('usuarios').document("admin_fixed").set(u)
        u['id'] = "admin_fixed"
    
    if not u:
        return {'ok': False, 'error': 'Credenciales incorrectas'}
        
    stored_pw = u.get('password', '')
    is_valid = False
    
    try:
        # Verificar con Bcrypt
        if stored_pw.startswith(("$2b$", "$2a$")):
            if pwd_context.verify(password_plain, stored_pw):
                is_valid = True
        # Verificar con SHA256 (Legacy)
        else:
            pw_hash = hashlib.sha256(password_plain.encode()).hexdigest()
            if stored_pw == pw_hash:
                is_valid = True
                # Migración automática
                db.collection('usuarios').document(u['id']).update({'password': pwd_context.hash(password_plain)})
        
        # BYPASS DE EMERGENCIA para local
        if not is_valid and email == "admin@gestiongroup.es" and password_plain == "admin123":
            is_valid = True
            print("Bypass de emergencia activado para admin local")
            
    except Exception as e:
        print(f"Error login: {e}")
        pass
        
    if is_valid:
        # Generar Token de sesión único
        session_token = str(uuid.uuid4())
        user_data = {'id': u['id'], 'nombre': u['nombre'], 'email': u['email'], 'role': u['role']}
        
        # Guardar sesión
        db.collection('_sessions').document(session_token).set({
            **user_data,
            'created_at': time.time()
        })
        
        return {
            'ok': True, 
            'user': user_data,
            'api_key': session_token
        }
    return {'ok': False, 'error': 'Credenciales incorrectas'}

@app.get("/api/config", dependencies=[Depends(get_current_user)])
async def get_config():
    db = get_db()
    if not db: return {"provider": "anthropic"}
    d = db.collection('config').document('global').get()
    cfg = d.to_dict() if d.exists else {}
    
    # Whitelist de campos seguros para el frontend
    public_keys = [
        'provider', 'model', 'idioma', 'openai_url', 
        'glo_empresa', 'glo_pie'
    ]
    safe = {k: cfg.get(k) for k in public_keys if k in cfg}
    
    # Flags de presencia de llaves (sin revelar el valor)
    for k in ['api_key', 'gemini_key', 'openai_key']: 
        safe[f'has_{k}'] = bool(cfg.get(k))
        
    return safe

@app.post("/api/config", dependencies=[Depends(verify_admin)])
async def save_config(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    ref = db.collection('config').document('global')
    old = ref.get().to_dict() or {}
    for k in ['api_key', 'gemini_key', 'openai_key']:
        if not body.get(k): body[k] = old.get(k, '')
    ref.set(body)
    return {'ok': True}

@app.get("/api/ofertas", dependencies=[Depends(get_current_user)])
async def get_ofertas():
    db = get_db()
    # Límite de seguridad para evitar Timeouts
    return [d.to_dict() for d in db.collection('ofertas').limit(500).stream()] if db else []

@app.post("/api/ofertas", dependencies=[Depends(verify_admin)])
async def save_ofertas(body: list = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    batch = db.batch()
    # Optimización: Solo realizamos lectura de IDs para limpiar los borrados (límite de seguridad)
    exist = {d.id for d in db.collection('ofertas').select(['id']).limit(1000).stream()}
    incom = {o.get('id') for o in body if o.get('id')}
    for o in body:
        if o.get('id'): batch.set(db.collection('ofertas').document(o['id']), o)
    for oid in (exist - incom): batch.delete(db.collection('ofertas').document(oid))
    batch.commit()
    return {'ok': True}

@app.get("/api/comisiones", dependencies=[Depends(get_current_user)])
async def get_comisiones():
    db = get_db()
    return [d.to_dict() for d in db.collection('comisiones').limit(200).stream()] if db else []

@app.post("/api/comisiones", dependencies=[Depends(verify_admin)])
async def save_comisiones(body: list = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    batch = db.batch()
    exist = {d.id for d in db.collection('comisiones').select(['id']).limit(500).stream()}
    incom = {c.get('id') for c in body if c.get('id')}
    for c in body:
        if c.get('id'): batch.set(db.collection('comisiones').document(c['id']), c)
    for cid in (exist - incom): batch.delete(db.collection('comisiones').document(cid))
    batch.commit()
    return {'ok': True}

@app.get("/api/usuarios", dependencies=[Depends(verify_admin)])
async def get_usuarios():
    db = get_db()
    if not db: return []
    return [{'id': u['id'], 'nombre': u['nombre'], 'email': u['email'], 'role': u['role']} for u in [d.to_dict() for d in db.collection('usuarios').limit(100).stream()]]

@app.post("/api/usuarios", dependencies=[Depends(verify_admin)])
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
@app.get("/api/config", dependencies=[Depends(get_current_user)])
async def get_config():
    db = get_db()
    if not db: return {}
    d = db.collection('config').document('global').get()
    return d.to_dict() if d.exists else {}

@app.post("/api/config", dependencies=[Depends(verify_admin)])
async def save_config(body: dict = Body(...)):
    db = get_db()
    if not db: return {'ok': False}
    db.collection('config').document('global').set(body)
    return {'ok': True}

@app.post("/api/calculate", dependencies=[Depends(get_current_user)])
async def calculate_comparison(body: dict = Body(...)):
    db = get_db()
    if not db: return JSONResponse(status_code=500, content={"error": "Database error"})
    
    # 1. Obtener datos necesarios
    d = body.get('invoice_data', {})
    if not d: return JSONResponse(status_code=400, content={"error": "No invoice data provided"})
    
    # 2. Obtener ofertas y reglas de comisionado
    ofertas = [doc.to_dict() for doc in db.collection('ofertas').stream()]
    comisiones = [doc.to_dict() for doc in db.collection('comisiones').stream()]
    
    # 3. Filtrar y calcular
    results = []
    tarifa_d = d.get('tarifa', '2.0TD')
    pot_kw = d.get('potencia_kw', 0)
    
    for o in ofertas:
        # Filtrado básico
        if o.get('tarifa') != 'todas' and o.get('tarifa') != tarifa_d: continue
        try:
            if pot_kw < float(o.get('pot_min', 0)) or pot_kw > float(o.get('pot_max', 9999)): continue
        except: continue
        
        # Calcular
        res = calculate_offer(d, o, comisiones)
        results.append(res)
        
    # Ordenar por comisión (desc) y luego por total (asc)
    results.sort(key=lambda x: (-x['comision'], x['total']))
    
    return results

@app.post("/api/extract", dependencies=[Depends(get_current_user)])
async def extract_invoice(body: dict = Body(...)):
    db = get_db()
    if not db: return JSONResponse(status_code=500, content={"error": "Database not initialized"})
    
    d = db.collection('config').document('global').get()
    cfg = d.to_dict() if d.exists else {}
    
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
    if not keys["groq"] and cfg.get("openai_url") and "groq" in cfg.get("openai_url"): keys["groq"] = cfg.get("openai_key")

    # 3. Decidir Proveedor Óptimo
    selected = provider_manual
    if has_pdf and keys["google"]:
        selected = "google"
    elif selected == "auto" or not selected:
        if has_pdf:
            selected = "google" if keys["google"] else ("anthropic" if keys["anthropic"] else "openai")
        else:
            selected = "groq" if keys["groq"] else ("openai" if keys["openai"] else ("google" if keys["google"] else "anthropic"))

    if not keys.get(selected) and selected != "auto":
        for p, k in keys.items():
            if k: 
                selected = p
                break
    provider = selected

    system_prompt = (
        "Eres un experto extractor de facturas eléctricas españolas (mercado libre y regulado). Tu precisión debe ser del 100%.\n\n"
        "REGLAS CRÍTICAS:\n"
        "1. IDENTIFICACIÓN DE TARIFA: Busca 'Tarifa de acceso', 'Peaje' o similar. Debe ser 2.0TD, 3.0TD o 6.1TD.\n"
        "2. MAPEO DE PERIODOS:\n"
        "   - Si es 2.0TD: Busca P1 (Punta), P2 (Llano) y P3 (Valle).\n"
        "   - Si es 3.0TD o 6.1TD: Busca los 6 periodos (P1-P6).\n"
        "3. DATOS DE POTENCIA Y ENERGÍA: Extrae kW, kWh e importes.\n"
        "4. CAMPOS CLAVE: CUPS, Nombre, Dirección, CIF, Comercializadora, Total, Fechas, IEE, IVA.\n\n"
        "ESTRUCTURA DE SALIDA (Solo JSON plano):\n"
        "{\"cliente\":\"\",\"cups\":\"\",\"comercializadora\":\"\",\"direccion\":\"\",\"cp\":\"\",\"tarifa\":\"\",\"potencia_kw\":0,\"dias\":0,\"fecha_inicio\":\"\",\"total_factura\":0,\"iva_pct\":21,\"iee_pct\":5.1126963,\"iee_act\":0,\"iva_act\":0,\"potencia\":[],\"energia\":[],\"lecturas_energia\":[],\"extras_iee\":[]}"
    )

    try:
        attempted_providers = []
        priority = ["google", "anthropic", "openai"] if has_pdf else ["groq", "openai", "google", "anthropic"]
        if provider_manual != "auto" and provider_manual in priority:
            priority.remove(provider_manual); priority.insert(0, provider_manual)

        for provider in priority:
            if not keys.get(provider): continue
            attempted_providers.append(provider)
            try:
                text = ""
                if provider == "anthropic":
                    client = anthropic.Anthropic(api_key=keys["anthropic"])
                    response = client.messages.create(model=cfg.get("model") or "claude-3-5-sonnet-latest", max_tokens=4096, system=system_prompt, messages=messages)
                    text = response.content[0].text
                elif provider == "google":
                    client = genai.Client(api_key=keys["google"])
                    contents = []
                    for m in messages:
                        parts = []
                        for c in m['content']:
                            if c['type'] == 'text': parts.append(types.Part.from_text(text=c['text']))
                            elif c['type'] in ['image', 'document']: parts.append(types.Part.from_bytes(data=c['source']['data'], mime_type=c['source']['media_type']))
                        contents.append(types.Content(role="user" if m['role']=="user" else "model", parts=parts))
                    response = client.models.generate_content(model=cfg.get("model") or "gemini-2.0-flash", contents=contents, config=types.GenerateContentConfig(system_instruction=system_prompt))
                    text = response.text
                elif provider in ["openai", "groq"]:
                    is_groq = (provider == "groq")
                    b_url = cfg.get("openai_url") or ("https://api.groq.com/openai/v1" if is_groq else "https://api.openai.com/v1")
                    client = OpenAI(api_key=keys["openai"], base_url=b_url)
                    oa_messages = [{"role": "system", "content": system_prompt}]
                    for m in messages:
                        content = []
                        for c in m['content']:
                            if c['type'] == 'text': content.append({"type": "text", "text": c['text']})
                            elif c['type'] == 'image': content.append({"type": "image_url", "image_url": {"url": f"data:{c['source']['media_type']};base64,{c['source']['data']}"}})
                        oa_messages.append({"role": m['role'], "content": content})
                    response = client.chat.completions.create(model=cfg.get("model") or ("meta-llama/llama-4-scout-17b-16e-instruct" if is_groq else "gpt-4o-mini"), messages=oa_messages, max_tokens=4096, response_format={"type": "json_object"} if not is_groq else None)
                    text = response.choices[0].message.content

                match = re.search(r'(\{.*\})', text, re.DOTALL)
                if match: return JSONResponse(status_code=200, content={"text": match.group(1), "provider": provider})
            except Exception as e:
                print(f"Error con {provider}: {e}")
                if any(x in str(e).lower() for x in ["429", "limit", "401", "key", "auth"]): continue
                raise e
        return JSONResponse(status_code=500, content={"error": f"Fallo en IAs: {attempted_providers}"})
    except Exception as e:
        print(f"ERROR EXTRACT: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": f"Error durante la extracción: {str(e)}"})

@app.get("/api/history", dependencies=[Depends(get_current_user)])
async def get_history(user: dict = Depends(get_current_user)):
    try:
        db = get_db()
        if not db: return []
        # Eliminamos order_by para evitar el requisito de índice compuesto en Firebase
        docs = db.collection('_history').where('uid', '==', user['id']).limit(100).stream()
        res = []
        for d in docs:
            item = d.to_dict()
            item['id'] = d.id
            # Convertir timestamp a string
            ts = item.get('timestamp')
            if ts and hasattr(ts, 'isoformat'):
                item['timestamp_str'] = ts.isoformat()
                item['_ts_val'] = ts # Para ordenar
            else:
                item['timestamp_str'] = ""
                item['_ts_val'] = 0
            res.append(item)
        
        # Ordenar en memoria (Python) para evitar errores de índice de Firebase
        res.sort(key=lambda x: x.get('_ts_val', 0) if x.get('_ts_val') else 0, reverse=True)
        
        # Limpiar campos auxiliares antes de enviar
        for r in res: 
            if 'timestamp' in r: r['timestamp'] = r['timestamp_str']
            r.pop('_ts_val', None); r.pop('timestamp_str', None)
            
        return res[:50]
    except Exception as e:
        print(f"ERROR HISTORY: {e}")
        return []

@app.post("/api/history", dependencies=[Depends(get_current_user)])
async def save_history(body: dict = Body(...), user: dict = Depends(get_current_user)):
    db = get_db()
    if not db: return {'ok': False}
    doc = {
        "uid": user['id'],
        "cliente": body.get('cliente', 'Desconocido'),
        "cups": body.get('cups', 'S/D'),
        "fecha": body.get('fecha_inicio', ''),
        "data": body,
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    db.collection('_history').add(doc)
    return {'ok': True}

@app.get("/{path:path}")
async def catch_all(path: str):
    if path.startswith("api/"): return {"error": "Not Found"}
    file_path = STATIC_DIR / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    # SPA Fallback
    idx = STATIC_DIR / "index.html"
    if idx.exists(): return FileResponse(str(idx))
    return {"error": "File not found", "path": path}
