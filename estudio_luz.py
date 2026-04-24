#!/usr/bin/env python3
"""
ESTUDIO LUZ v2.0
================
Doble clic en INICIAR.bat para arrancar.
Luego abre Chrome en: http://localhost:8765
"""

import http.server, json, urllib.request, urllib.error, os, webbrowser, threading, time, hashlib
from pathlib import Path

PORT = 8766
BASE = Path(__file__).parent
DB_OFERTAS  = BASE / 'ofertas_db.json'
DB_USUARIOS = BASE / 'usuarios_db.json'
DB_CONFIG   = BASE / 'config_db.json'
DB_COMISIONES = BASE / 'comisiones_db.json'

# ── HELPERS ──────────────────────────────────────────────────────────────────
def load_json(path, default):
    try:
        if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    except: pass
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def init_defaults():
    if not DB_USUARIOS.exists():
        save_json(DB_USUARIOS, [
            {"id":"1","nombre":"Administrador","email":"admin@gestiongroup.es","password":hash_pw("admin123"),"role":"admin"},
            {"id":"2","nombre":"Comercial Demo","email":"comercial@gestiongroup.es","password":hash_pw("comercial123"),"role":"comercial"}
        ])
    if not DB_CONFIG.exists():
        save_json(DB_CONFIG, {"api_key":"","idioma":"es"})
    if not DB_OFERTAS.exists():
        save_json(DB_OFERTAS, [])

init_defaults()

# ── HTML ──────────────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estudio Luz</title>
<link rel="icon" type="image/png" href="https://gestiongroup.es/wp-content/uploads/2024/07/Logotipo-Gestion-Group.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --primary: #2cb5ad;
  --primary-soft: rgba(44, 181, 173, 0.1);
  --primary-deep: #249992;
  --bg: #f8fafc;
  --bg-card: #ffffff;
  --tx: #0f172a;
  --t2: #475569;
  --t3: #94a3b8;
  --border: #e2e8f0;
  --ok: #10b981;
  --warn: #f59e0b;
  --err: #ef4444;
  --radius: 8px;
  --radius-lg: 12px;
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  --shadow: 0 4px 6px -1px rgba(0,0,0,0.05);

  /* COMPATIBILIDAD CON JS ANTIGUO */
  --acc: var(--primary);
  --acc2: var(--primary);
  --b1: var(--border);
  --b2: var(--border);
}

* { box-sizing: border-box; margin: 0; padding: 0; font-smooth: antialiased; }
body { background: var(--bg); color: var(--tx); font-family: 'Inter', system-ui, sans-serif; font-size: 13px; line-height: 1.5; min-height: 100vh; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
.anim-in { animation: fadeIn 0.4s ease-out forwards; }

.login-screen { position: fixed; inset: 0; background: #fff; display: flex; align-items: center; justify-content: center; z-index: 999; }
.login-box { background: #fff; border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 40px; width: 380px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); text-align: center; }
.login-logo { margin-bottom: 30px; }
.login-logo .brand { font-weight: 800; font-size: 24px; color: #1e293b; letter-spacing: -0.02em; }
.login-logo .brand span { color: var(--primary); }
.login-logo .sub { font-size: 10px; color: var(--t3); letter-spacing: 1px; text-transform: uppercase; margin-top: 4px; }

.login-field { margin-bottom: 20px; text-align: left; }
.login-field label { display: block; font-size: 11px; color: var(--t2); font-weight: 600; margin-bottom: 6px; }
.login-field input { width: 100%; border: 1px solid var(--border); border-radius: var(--radius); padding: 10px 12px; font-size: 13px; transition: var(--transition); }
.login-field input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-soft); }
.login-err { background: #fef2f2; color: var(--err); font-size: 12px; padding: 10px; border-radius: 6px; margin-bottom: 20px; text-align: center; }
.login-btn { width: 100%; padding: 12px; background: var(--primary); color: white; font-weight: 700; border: none; border-radius: var(--radius); cursor: pointer; transition: var(--transition); }
.login-btn:hover { background: var(--primary-deep); transform: translateY(-1px); }

.shell { display: flex; flex-direction: column; height: 100vh; }
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 0 24px; height: 60px; background: #fff; border-bottom: 1px solid var(--border); }
.logo { font-weight: 800; font-size: 18px; display: flex; align-items: center; gap: 8px; color: #1e293b; }
.logo-bolt { color: var(--primary); }
.logo span { color: var(--primary); }

.tabs { display: flex; gap: 4px; background: #f1f5f9; padding: 4px; border-radius: 10px; }
.tab { padding: 6px 16px; border-radius: 7px; cursor: pointer; font-weight: 600; font-size: 11px; color: var(--t2); background: transparent; border: none; transition: var(--transition); }
.tab:hover { background: rgba(255,255,255,0.5); }
.tab.on { background: #fff; color: var(--primary); box-shadow: 0 1px 2px rgba(0,0,0,0.05); }

.user-info { display: flex; align-items: center; gap: 16px; }
.user-badge { font-size: 12px; font-weight: 600; color: var(--t2); }
.user-badge .role { font-size: 10px; color: var(--t3); background: #f1f5f9; padding: 2px 8px; border-radius: 4px; margin-left: 8px; text-transform: uppercase; }
.btn-logout { background: transparent; color: var(--t3); border: none; cursor: pointer; font-size: 11px; font-weight: 600; }

.body { flex: 1; overflow: hidden; display: flex; }
.pane { flex: 1; overflow-y: auto; padding: 24px; }
.page { display: none; }
.page.on { display: block; }

.sec { font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--t3); margin-bottom: 16px; display: flex; align-items: center; gap: 12px; }
.sec::after { content: ''; flex: 1; height: 1px; background: var(--border); }

.card { background: #fff; border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 20px; box-shadow: var(--shadow); }
.ct { 
  font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 18px;
  display: flex; align-items: center; gap: 10px; font-family: 'Outfit', sans-serif;
  letter-spacing: -0.01em;
}
.ct::before { content: ''; width: 3px; height: 16px; background: var(--primary); border-radius: 4px; }

.g2, .g3, .g4 { display: grid; gap: 16px; }
.g2 { grid-template-columns: 1fr 1fr; }
.g3 { grid-template-columns: repeat(3, 1fr); }
.g4 { grid-template-columns: repeat(4, 1fr); }
.gfull { grid-column: span 2; }

.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 11px; color: var(--t2); font-weight: 600; margin-bottom: 6px; }
.field input, .field select { border: 1px solid var(--border); border-radius: var(--radius); padding: 8px 10px; color: var(--tx); font-size: 13px; transition: var(--transition); }
.field input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-soft); }
.field input[readonly] { background: #f8fafc; border-color: transparent; font-weight: 700; color: var(--primary); font-size: 16px; width: 100%; }

.ptbl { width: 100%; border-collapse: collapse; }
.ptbl th { font-size: 10px; color: var(--t3); text-transform: uppercase; text-align: left; padding: 8px; background: #f8fafc; border-bottom: 1px solid var(--border); }
.ptbl td { padding: 4px; border-bottom: 1px solid #f1f5f9; }
.ptbl input { width: 100%; border: 1px solid transparent; border-radius: 4px; padding: 4px 8px; font-size: 12px; text-align: right; }
.ptbl input:focus { background: #fff; border-color: var(--primary); outline: none; }

.btn { padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: var(--transition); border: 1px solid transparent; }
.btn-p { background: var(--primary); color: white; }
.btn-p:hover { background: var(--primary-deep); }
.btn-ai { background: #1e293b; color: white; }
.btn-s { background: #fff; color: var(--t2); border-color: var(--border); }
.btn-d { 
  background: #fff1f2; color: #e11d48; width: 32px; height: 32px; 
  display: flex; align-items: center; justify-content: center; 
  border-radius: 50%; border: 1px solid #fecaca; font-size: 14px;
}
.btn-d:hover { background: #be123c; color: white; border-color: #be123c; transform: scale(1.1); box-shadow: 0 4px 10px rgba(190, 18, 60, 0.2); }
.btn-sm { padding: 4px 10px; font-size: 11px; }

.ai { background-color: #f0fdfa !important; border-color: #99f6e4 !important; }
.unc { background-color: #fffbeb !important; border-color: #fde68a !important; }

.sb-bar { display: flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 8px; font-size: 12px; margin-bottom: 16px; }
.sb-bar.load { background: #eff6ff; color: #3b82f6; }
.sb-bar.ok { background: #ecfdf5; color: var(--ok); }
.sb-bar.err { background: #fef2f2; color: var(--err); }

.upzone { border: 2px dashed var(--border); border-radius: var(--radius-lg); padding: 32px; text-align: center; cursor: pointer; background: #f8fafc; transition: var(--transition); }
.upzone:hover { border-color: var(--primary); background: #f0fdfa; }
.up-icon { font-size: 32px; margin-bottom: 8px; }
.up-title { font-weight: 700; font-size: 15px; color: #1e293b; }
.up-sub { font-size: 11px; color: var(--t3); }

.ofr-card { background: #fff; border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; margin-bottom: 12px; cursor: pointer; transition: var(--transition); }
.ofr-card:hover { border-color: var(--primary); box-shadow: var(--shadow); }
.ofr-card.sel { border-color: var(--primary); background: #f0fdfa; box-shadow: 0 0 0 2px var(--primary-soft); }
.ofr-name { font-weight: 700; color: #1e293b; }
.ofr-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 12px; }
.met-l { font-size: 10px; color: var(--t3); text-transform: uppercase; }
.met-v { font-size: 14px; font-weight: 700; }
.met-v.g { color: var(--ok); }
.met-v.r { color: var(--err); }

/* COMPARATIVA & COMISIONADO STYLES */
.trow { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 12px; }
.trow-l { color: var(--t2); }
.ahorro-box { background: #ecfdf5; border-radius: 8px; padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-top: 16px; border: 1px solid #10b98133; }
.ahorro-v { font-size: 22px; font-weight: 800; color: var(--ok); font-family: 'Outfit'; }
.com-box { border-top: 1px dashed var(--border); margin-top: 16px; padding-top: 12px; }
.com-v { font-size: 18px; font-weight: 700; color: #b45309; }
.com-item { padding: 10px 12px; border-radius: 6px; cursor: pointer; transition: 0.2s; border: 1px solid transparent; }
.com-item:hover { background: var(--bg); }
.com-item.active { background: var(--primary-soft); border-color: var(--primary); font-weight: 700; color: var(--primary); }
.bdg { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; }
.bdg-g { background: #dcfce7; color: #15803d; }
.bdg-b { background: #dbeafe; color: #1d4ed8; }

.abar { display: flex; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border); }

@media (max-width: 768px) { .g2, .g3, .g4 { grid-template-columns: 1fr; } }

.modal-bg { position: fixed; inset: 0; background: rgba(15,23,42,0.5); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; z-index: 1000; padding: 20px; }
.modal { background: #fff; border-radius: var(--radius-lg); padding: 32px; width: 100%; max-width: 800px; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); animation: fadeIn 0.3s ease-out; }
.modal-title { font-size: 18px; font-weight: 800; color: #1e293b; margin-bottom: 24px; display: flex; align-items: center; gap: 10px; }
.modal-title::before { content: '✎'; color: var(--primary); }

.toggle-row { display: flex; align-items: center; gap: 10px; font-weight: 600; color: var(--t2); margin-bottom: 12px; }
.info-box, .warn-box { padding: 12px 16px; border-radius: 8px; font-size: 12px; margin-bottom: 16px; }
.info-box { background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; }
.warn-box { background: #fffbeb; color: #b45309; border: 1px solid #fef3c7; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
.tag.t { background: var(--primary-soft); color: var(--primary); }
</style>
</head>
<body>

<!-- ══ LOGIN ══ -->
<div class="login-screen" id="loginScreen">
  <div class="login-box">
    <div class="login-logo">
      <div class="brand">ESTUDIO <span>LUZ</span></div>
      <div class="sub">Gestion Group · Soluciones Energéticas</div>
    </div>
    <div class="login-field"><label>Correo Electrónico</label><input type="email" id="l_email" placeholder="usuario@gestiongroup.es"></div>
    <div class="login-field"><label>Contraseña</label><input type="password" id="l_pass" placeholder="••••••••" onkeydown="if(event.key==='Enter') doLogin()"></div>
    <div class="login-err" id="l_err">Credenciales incorrectas</div>
    <button class="login-btn" onclick="doLogin()">Acceder al Sistema</button>
  </div>
</div>

<!-- ══ APP ══ -->
<div class="shell" id="shell">
  <div class="topbar">
    <div class="logo"><span class="logo-bolt">⚡</span>ESTUDIO <span>LUZ</span></div>
    <div class="tabs" id="mainTabs">
      <button class="tab on"  onclick="go('fac')"  id="tab-fac">① Factura</button>
      <button class="tab"     onclick="go('rev')"  id="tab-rev">② Revisión</button>
      <button class="tab"     onclick="go('cmp')"  id="tab-cmp">③ Comparativa</button>
      <button class="tab"     onclick="go('ofr')"  id="tab-ofr">Base de Ofertas</button>
      <button class="tab"     onclick="go('com')"  id="tab-com">Comisionado</button>
      <button class="tab"     onclick="go('cfg')"  id="tab-cfg">Configuración</button>
    </div>
    <div class="user-info">
      <div class="user-badge">
        <span id="ui_nombre">—</span>
        <span class="role" id="ui_role">—</span>
      </div>
      <button class="btn-logout" onclick="doLogout()">Salir</button>
    </div>
  </div>
  <div class="body"><div class="pane">

    <!-- ══ FACTURA APORTADA ══ -->
    <div class="page on" id="p-fac">
      <!-- Asesor + fecha -->
      <div class="g2" style="margin-bottom:16px">
        <div class="field"><label>Asesor Energético</label>
          <input id="g_asesor" placeholder="Nombre completo" oninput="localStorage.setItem('el_asesor',this.value)">
        </div>
        <div class="field"><label>Fecha de Propuesto</label>
          <input type="date" id="g_fecha">
        </div>
      </div>

      <!-- Upload -->
      <div class="sec">Subir factura</div>
      <div class="upzone" id="upzone">
        <input type="file" id="fInput" accept=".pdf,.jpg,.jpeg,.png,.webp" multiple onchange="onFiles(this.files)">
        <div class="up-icon">📂</div>
        <div class="up-title">Arrastra tu factura aquí</div>
        <div class="up-sub" id="upSub">PDF o imágenes · Se permiten varias páginas</div>
      </div>
      <div id="chips" style="margin-top:8px;display:flex;flex-wrap:wrap;gap:6px"></div>
      <div id="sb" style="display:none;margin-top:10px"></div>

      <div id="prevSec" style="display:none;margin-top:12px">
        <img id="prevImg" class="prev-img" style="display:none">
        <div style="display:flex;gap:8px;margin-top:8px">
          <button class="btn btn-ai" id="btnEx" onclick="extract()">✦ Extraer con IA</button>
          <button class="btn btn-s btn-sm" onclick="resetUp()">Cambiar archivos</button>
        </div>
      </div>

      <!-- Consumo anual CUPS -->
      <div class="card" style="margin-top:16px">
        <div class="ct">Parámetros del CUPS</div>
        <div class="g3">
          <div class="field"><label>CONSUMO ANUAL TOTAL (kWh)</label>
            <input type="number" id="f_consumo_anual" step="1" placeholder="Ej: 45000">
          </div>
          <div class="field"><label>POTENCIA CONTRATADA (kW)</label>
            <input type="number" id="f_pot_cups" step=".001" placeholder="Ej: 25" onchange="syncPot()">
          </div>
          <div class="field"><label>TARIFA DETECTADA</label>
            <select id="f_tar_cups" onchange="syncTar(this.value)" style="color:var(--acc2);font-weight:700">
              <option value="2.0TD">2.0TD</option>
              <option value="3.0TD">3.0TD</option>
              <option value="6.1TD">6.1TD</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ REVISIÓN ══ -->
    <div class="page" id="p-rev">
      <div style="display:flex;gap:14px;margin-bottom:12px;font-size:11px;color:var(--t2)">
        <span><span style="display:inline-block;width:10px;height:10px;background:rgba(87,212,255,.5);border-radius:2px;margin-right:4px"></span>Extraído por IA</span>
        <span><span style="display:inline-block;width:10px;height:10px;background:rgba(245,200,66,.5);border-radius:2px;margin-right:4px"></span>Requiere verificación</span>
      </div>

      <div class="card">
        <div class="ct">Datos del cliente</div>
        <div class="g2">
          <div class="field gfull"><label>CLIENTE / RAZÓN SOCIAL</label><input id="f_cli"></div>
          <div class="field"><label>CUPS</label><input id="f_cups"></div>
          <div class="field"><label>COMERCIALIZADORA ACTUAL</label><input id="f_com"></div>
          <div class="field gfull"><label>DIRECCIÓN</label><input id="f_dir"></div>
          <div class="field"><label>CÓDIGO POSTAL</label><input id="f_cp"></div>
          <div class="field"><label>TARIFA</label>
            <select id="f_tar" onchange="syncTar(this.value)" style="font-weight:700">
              <option value="2.0TD">2.0TD</option>
              <option value="3.0TD">3.0TD</option>
              <option value="6.1TD">6.1TD</option>
            </select>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="ct">Parámetros de facturación</div>
        <div class="g3">
          <div class="field"><label>POTENCIA CONTRATADA (kW)</label><input type="number" id="f_pot" step=".001" onchange="updTar()"></div>
          <div class="field"><label>DÍAS FACTURADOS</label><input type="number" id="f_dias"></div>
          <div class="field"><label>FECHA INICIO PERÍODO</label><input type="date" id="f_fi"></div>
          <div class="field"><label>TOTAL FACTURA (€) ⚠</label><input type="number" id="f_tot" step=".01" class="unc"></div>
          <div class="field"><label>IVA / IGIC (%)</label><input type="number" id="f_iva" value="21" step=".01"></div>
          <div class="field"><label>IEE (%)</label><input type="number" id="f_iee" value="5.1126963" step=".0001"></div>
          <div class="field"><label>IEE FACTURA ACTUAL (€)</label><input type="number" id="f_iee_act" step=".01" value="0"></div>
          <div class="field"><label>IVA FACTURA ACTUAL (€)</label><input type="number" id="f_iva_act" step=".01" value="0"></div>
          <div class="field"><label>DESCUENTO ENERGÍA ACTUAL (%)</label><input type="number" id="f_dto_en_act" step=".01" value="0"></div>
        </div>
      </div>

      <!-- Facturas con 2 períodos de precio -->
      <div class="card">
        <div class="ct">Períodos de precio</div>
        <div class="toggle-row">
          <input type="checkbox" id="f_dos_periodos" onchange="togDosPeriodos()">
          <label for="f_dos_periodos">Esta factura tiene múltiples períodos de precio</label>
        </div>
        <div id="dosPeriodosInfo" class="info-box" style="display:none">
          Al activar esta opción, puedes añadir más de 1 línea por período de potencia y energía. La inteligencia artificial creará tantas filas como sub-períodos detecte.
        </div>
      </div>

      <div class="card">
        <div class="ct" style="display:flex;justify-content:space-between;align-items:center">
          <span>Término de potencia — P1 a P6 <span class="tag t" id="tarTag">2.0TD</span></span>
          <div id="addPotBtn" style="display:none">
            <select id="addPotSel" style="font-size:10px;padding:2px;border-radius:3px;background:var(--bg);color:var(--tx);border:1px solid var(--b1)"><option>P1</option><option>P2</option><option>P3</option><option>P4</option><option>P5</option><option>P6</option></select>
            <button class="btn btn-s btn-sm" onclick="addPotL()">+ Fila</button>
          </div>
        </div>
        <div class="warn-box" id="potHint" style="display:none">En 3.0TD/6.1TD cada periodo puede tener distinta potencia contratada. Ajusta los kW por periodo si es necesario.</div>
        <table class="ptbl">
          <thead><tr><th style="width:50px">PER</th><th>kW</th><th>IMPORTE (€)</th><th style="width:30px"></th></tr></thead>
          <tbody id="potT"></tbody>
        </table>
      </div>

      <div class="card">
        <div class="ct" style="display:flex;justify-content:space-between;align-items:center">
          <span>Término de energía — P1 a P6</span>
          <div id="addEnBtn" style="display:none">
            <select id="addEnSel" style="font-size:10px;padding:2px;border-radius:3px;background:var(--bg);color:var(--tx);border:1px solid var(--b1)"><option>P1</option><option>P2</option><option>P3</option><option>P4</option><option>P5</option><option>P6</option></select>
            <button class="btn btn-s btn-sm" onclick="addEnL()">+ Fila</button>
          </div>
        </div>
        <table class="ptbl">
          <thead><tr><th style="width:50px">PER</th><th>kWh</th><th>€/kWh</th><th style="width:30px"></th></tr></thead>
          <tbody id="enT"></tbody>
        </table>
      </div>

      <div class="card" id="lecCard">
        <div class="ct" style="display:flex;justify-content:space-between;align-items:center;color:var(--acc2)">
          <span>Lecturas Reales (Desglose para simulación)</span>
          <div id="addLecBtn">
            <select id="addLecSel" style="font-size:10px;padding:2px;border-radius:3px;background:var(--bg);color:var(--tx);border:1px solid var(--b1)"><option>P1</option><option>P2</option><option>P3</option><option>P4</option><option>P5</option><option>P6</option></select>
            <button class="btn btn-s btn-sm" onclick="addLecL()">+ Fila</button>
          </div>
        </div>
        <div style="font-size:11px;color:var(--t2);margin-bottom:10px;line-height:1.4">Opcional. Si la factura agrupó meses o no detalla kWh en Facturación, usa esta tabla para introducir las verdaderas lecturas de contador. La simulación de "Nueva Oferta" y su ahorro se basará en estos datos si existen.</div>
        <table class="ptbl">
          <thead><tr><th style="width:50px">PER</th><th>kWh</th><th style="width:30px"></th></tr></thead>
          <tbody id="lecT"></tbody>
        </table>
      </div>

      <!-- Autoconsumo -->
      <div class="card">
        <div class="ct">Autoconsumo</div>
        <div class="toggle-row">
          <input type="checkbox" id="f_tiene_autocon" onchange="togAutocon()">
          <label for="f_tiene_autocon">Esta factura tiene autoconsumo</label>
        </div>
        <div id="autoconFields" style="display:none">
          <div class="g3">
            <div class="field"><label>kWh GENERADOS / COMPENSADOS</label><input type="number" id="f_aut_kwh" step=".001" value="0"></div>
            <div class="field"><label>€/kWh PRECIO COMPENSACIÓN ACTUAL</label><input type="number" id="f_aut_precio" step=".000001" value="0"></div>
            <div class="field"><label>TOTAL COMPENSACIÓN (€)</label><input type="number" id="f_aut_total" step=".01" value="0" readonly style="color:var(--ok)"></div>
          </div>
          <div style="font-size:11px;color:var(--t2);margin-top:8px">La compensación se calculará automáticamente: kWh × €/kWh</div>
        </div>
      </div>

      <div class="card">
        <div class="ct">Conceptos adicionales</div>
        <div class="g2">
          <div class="field"><label>ENERGÍA REACTIVA (€)</label><input type="number" id="f_rea" value="0" step=".01"></div>
          <div class="field"><label>EXCESO POTENCIA (€)</label><input type="number" id="f_exc" value="0" step=".01"></div>
          <div class="field"><label>ALQUILER EQUIPOS (€)</label><input type="number" id="f_alq" value="0" step=".01"></div>
          <div class="field"><label>BONO SOCIAL / FINANCIACIÓN (€)</label><input type="number" id="f_bon" value="0" step=".01"></div>
          <div class="field"><label>SERVICIO / OTROS (Sin IVA) (€)</label><input type="number" id="f_ser" value="0" step=".01"></div>
        </div>
      </div>

      <div class="card">
        <div class="ct">Otros conceptos sujetos a IEE</div>
        <div id="ieeExtras"></div>
        <button class="btn btn-s btn-sm" style="margin-top:6px" onclick="addIeeExtra()">+ Añadir concepto</button>
      </div>

      <div class="abar">
        <button class="btn btn-p" onclick="go('cmp')">Siguiente → Comparativa</button>
        <button class="btn btn-s" onclick="go('fac')">← Volver</button>
      </div>
    </div>

    <!-- ══ COMPARATIVA ══ -->
    <div class="page" id="p-cmp">
      <div class="cmp-grid">
        <div>
          <div class="sec">Facturación actual</div>
          <div class="card" id="actCard"><div class="empty"><div class="eico">📋</div>Cargando...</div></div>
          <div class="sec" style="margin-top:18px">Ranking de ofertas</div>
          <div id="rankDiv"></div>
        </div>
        <div>
          <div class="sec">Oferta seleccionada</div>
          <div id="detDiv"><div class="empty"><div class="eico">👈</div>Selecciona una oferta</div></div>
          <div class="abar" style="flex-direction:column;margin-top:10px">
            <button class="btn btn-p" style="width:100%" onclick="genPDF()">📄 Generar PDF para comercial</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ OFERTAS DB (solo admin) ══ -->
    <div class="page" id="p-ofr">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px">
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:800;font-size:18px">Base de Datos de Ofertas</div>
          <div style="color:var(--t2);font-size:11px;margin-top:3px">Tarifas disponibles · se guardan en archivo local</div>
        </div>
        <button class="btn btn-p" onclick="openMod(null)">+ Nueva Oferta</button>
      </div>
      <div id="ofrList"></div>
    </div>

    <!-- ══ CONFIGURACIÓN ══ -->
    <div class="page" id="p-cfg">
      <!-- API KEY (solo admin) -->
      <div class="cfg-section" id="cfg-api">
        <div class="cfg-title">🔑 API Key Anthropic</div>
        <div class="g2">
          <div class="field gfull"><label>API KEY</label>
            <input type="password" id="cfg_apikey" placeholder="sk-ant-...">
          </div>
        </div>
        <div class="abar" style="border:none;padding:10px 0 0 0">
          <button class="btn btn-p btn-sm" onclick="saveConfig()">Guardar API Key</button>
        </div>
      </div>

      <!-- Idioma -->
      <div class="cfg-section">
        <div class="cfg-title">🌐 Idioma</div>
        <div class="g3">
          <div class="field"><label>IDIOMA DE LA INTERFAZ</label>
            <select id="cfg_idioma" onchange="saveConfig()">
              <option value="es">🇪🇸 Español</option>
              <option value="en">🇬🇧 English</option>
              <option value="ca">🏴 Català</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Gestión usuarios (admin: ve todos; comercial: solo el suyo) -->
      <div class="cfg-section">
        <div class="cfg-title" id="cfg-users-title">👤 Gestión de Usuarios</div>
        <div id="cfg-users-content"></div>
        <div class="abar" style="border:none;padding:10px 0 0 0" id="cfg-users-addbar">
          <button class="btn btn-p btn-sm" onclick="openUserMod(null)">+ Nuevo usuario</button>
        </div>
      </div>
    </div>

    <!-- PAGE COMISIONADO (Centralized) -->
    <div class="page" id="p-com">
      <div style="display:flex;gap:20px;height:calc(100vh - 180px)">
        <!-- Sidebar -->
        <div style="width:240px;display:flex;flex-direction:column;gap:12px">
          <div class="sec" style="margin:0;display:flex;justify-content:space-between;align-items:center">
            Comercializadoras
            <button class="btn btn-p btn-sm" onclick="addComCo()">+ Añadir</button>
          </div>
          <div id="comList" style="flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:4px">
            <!-- List of companies -->
          </div>
        </div>
        <!-- Main Editor -->
        <div style="flex:1;display:flex;flex-direction:column;gap:16px">
          <div id="comEditorEmpty" class="empty" style="margin-top:0">
            <div class="eico">🏦</div>
            Selecciona una comercializadora para configurar sus comisiones.
          </div>
          <div id="comEditor" class="card" style="display:none;margin:0;flex:1;overflow-y:auto">
            <div style="display:flex;justify-content:space-between;border-bottom:1px solid var(--b1);padding-bottom:12px;margin-bottom:16px">
              <h3 id="comCoName" style="font-family:'Outfit';color:var(--tx);margin:0">Nombre Empresa</h3>
              <div style="display:flex;gap:8px">
                <button class="btn btn-d" onclick="delComCo()">🗑️</button>
                <button class="btn btn-p btn-sm" onclick="saveComs()">Guardar Cambios</button>
              </div>
            </div>
            <div class="sec">Escalado de Comisiones (Tramos)</div>
            <div class="info-box" style="margin-bottom:12px">Define las reglas para esta empresa. El sistema aplicará la primera regla que coincida con la potencia y el consumo del cliente.</div>
            <table class="ptbl">
              <thead>
                <tr>
                  <th>Pot Min</th>
                  <th>Pot Max</th>
                  <th>Cons Min</th>
                  <th>Cons Max</th>
                  <th>Filtro Plan (Opcional)</th>
                  <th>Valor</th>
                  <th style="width:100px">Tipo</th>
                  <th style="width:30px"></th>
                </tr>
              </thead>
              <tbody id="comTramosT"></tbody>
            </table>
            <button class="btn btn-s btn-sm" onclick="addComTramo()" style="margin-top:12px">+ Añadir Tramo</button>
          </div>
        </div>
      </div>
    </div>

  </div></div>
</div>

<!-- MODAL OFERTA -->
<div class="modal-bg" id="modalOfr">
  <div class="modal">
    <div class="modal-title" id="modOfrT">Nueva Oferta</div>
    <div class="g2">
      <div class="field"><label>NOMBRE DE LA OFERTA</label><input id="o_nom" placeholder="Ej: Plan Fijo Premium"></div>
      <div class="field"><label>COMERCIALIZADORA</label><input id="o_com" placeholder="Ej: Iberdrola"></div>
      <div class="field"><label>TARIFA</label>
        <select id="o_tar">
          <option value="2.0TD">2.0TD</option>
          <option value="3.0TD">3.0TD</option>
          <option value="6.1TD">6.1TD</option>
          <option value="todas">Todas</option>
        </select>
      </div>
      <div class="field"><label>TIPO DE PRECIO</label>
        <select id="o_tip"><option value="FIJO">PRECIO FIJO</option><option value="INDEXADO">INDEXADO</option><option value="VARIABLE">VARIABLE</option></select>
      </div>
      <div class="field"><label>PERMANENCIA</label><input id="o_per" placeholder="Sin permanencia / 12 meses"></div>
      <div class="field"><label>VALIDEZ (días)</label><input type="number" id="o_val" value="7" min="1"></div>
    </div>

    <!-- Rango potencia y consumo -->
    <div class="sec" style="margin-top:14px">Rango de aplicación</div>
    <div class="g4">
      <div class="field"><label>POT. MÍNIMA (kW)</label><input type="number" id="o_pmin" value="0" step=".001"></div>
      <div class="field"><label>POT. MÁXIMA (kW)</label><input type="number" id="o_pmax" value="9999" step=".001"></div>
      <div class="field"><label>CONSUMO MÍN. (kWh/año)</label><input type="number" id="o_cmin" value="0" step="1"></div>
      <div class="field"><label>CONSUMO MÁX. (kWh/año)</label><input type="number" id="o_cmax" value="99999999" step="1"></div>
    </div>

    <!-- Comisión -->
    <div class="sec" style="margin-top:14px">Comisión</div>
    <div class="g2">
      <div class="field"><label>TIPO DE COMISIÓN</label>
        <select id="o_tco" onchange="togComision()">
          <option value="fijo">€ Fijo por contrato</option>
          <option value="consumo">Por consumo (Coef. × kWh × FEE / 1000)</option>
        </select>
      </div>
      <div class="field" id="f_comfijo"><label>COMISIÓN FIJA (€)</label><input type="number" id="o_co" step=".01" placeholder="Ej: 280"></div>
    </div>
    <div class="g3" id="f_comconsumo" style="display:none">
      <div class="field"><label>COEFICIENTE REPARTO (%)</label><input type="number" id="o_coef" step=".01" placeholder="Ej: 85"></div>
      <div class="field"><label>FEE (€/MWh)</label><input type="number" id="o_fee" step=".01" placeholder="Ej: 4.5"></div>
      <div class="field"><label>RESULTADO (se calcula automático)</label><input id="o_co_preview" readonly style="color:var(--acc)"></div>
    </div>

    <!-- Autoconsumo compensación -->
    <div class="g2" style="margin-top:10px">
      <div class="field"><label>COMPENSACIÓN AUTOCONSUMO (€/kWh)</label><input type="number" id="o_comp" step=".0001" value="0"></div>
      <div class="field"><label>DESCUENTO POTENCIA (%)</label><input type="number" id="o_dp" step=".1" value="0"></div>
    </div>
    <div class="g2">
      <div class="field"><label>DESCUENTO ENERGÍA GLOBAL (%)</label><input type="number" id="o_de" step=".1" value="0"></div>
      <div style="display:flex;align-items:center;gap:8px;padding-top:22px">
        <input type="checkbox" id="o_dpp" onchange="togDpp()" style="accent-color:var(--acc)">
        <label for="o_dpp" style="font-size:11px;color:var(--t2);cursor:pointer">Discriminar dto. energía por periodo</label>
      </div>
    </div>
    <div id="dppDet" style="display:none;margin-top:8px">
      <table class="ptbl"><thead><tr><th>P1 %</th><th>P2 %</th><th>P3 %</th><th>P4 %</th><th>P5 %</th><th>P6 %</th></tr></thead>
      <tbody><tr>
        <td><input type="number" id="o_de1" step=".1" value="0"></td>
        <td><input type="number" id="o_de2" step=".1" value="0"></td>
        <td><input type="number" id="o_de3" step=".1" value="0"></td>
        <td><input type="number" id="o_de4" step=".1" value="0"></td>
        <td><input type="number" id="o_de5" step=".1" value="0"></td>
        <td><input type="number" id="o_de6" step=".1" value="0"></td>
      </tr></tbody></table>
    </div>

    <div class="sec" style="margin-top:14px">Precios de potencia (€/kW/día)</div>
    <table class="ptbl"><thead><tr><th>P1</th><th>P2</th><th>P3</th><th>P4</th><th>P5</th><th>P6</th></tr></thead>
    <tbody><tr>
      <td><input type="number" id="o_pp1" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_pp2" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_pp3" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_pp4" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_pp5" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_pp6" step=".000001" placeholder="0"></td>
    </tr></tbody></table>

    <div class="sec" style="margin-top:12px">Precios de energía (€/kWh)</div>
    <table class="ptbl"><thead><tr><th>P1</th><th>P2</th><th>P3</th><th>P4</th><th>P5</th><th>P6</th></tr></thead>
    <tbody><tr>
      <td><input type="number" id="o_ep1" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_ep2" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_ep3" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_ep4" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_ep5" step=".000001" placeholder="0"></td>
      <td><input type="number" id="o_ep6" step=".000001" placeholder="0"></td>
    </tr></tbody></table>

    <div class="modal-foot">
      <button class="btn btn-s" onclick="closeMod('modalOfr')">Cancelar</button>
      <button class="btn btn-p" onclick="saveOfr()">Guardar Oferta</button>
    </div>
  </div>
</div>


<!-- MODAL USUARIO -->
<div class="modal-bg" id="modalUser">
  <div class="modal" style="width:420px">
    <div class="modal-title" id="modUserT">Nuevo Usuario</div>
    <div class="field" style="margin-bottom:12px"><label>NOMBRE</label><input id="u_nombre" placeholder="Ej: Juan García"></div>
    <div class="field" style="margin-bottom:12px"><label>EMAIL</label><input type="email" id="u_email" placeholder="juan@empresa.es"></div>
    <div class="field" style="margin-bottom:12px"><label>CONTRASEÑA <span style="color:var(--t3);font-size:10px">(dejar vacío para no cambiar)</span></label><input type="password" id="u_pass" placeholder="••••••••"></div>
    <div class="field" style="margin-bottom:12px" id="u_role_field"><label>PERFIL</label>
      <select id="u_role"><option value="comercial">Comercial</option><option value="admin">Administración</option></select>
    </div>
    <div class="modal-foot">
      <button class="btn btn-s" onclick="closeMod('modalUser')">Cancelar</button>
      <button class="btn btn-p" onclick="saveUser()">Guardar</button>
    </div>
  </div>
</div>

<script>

// ════════════════════════════════════════════
// I18N
// ════════════════════════════════════════════
const I18N = {
  en: {
    "CORREO ELECTRÓNICO": "EMAIL", "CONTRASEÑA": "PASSWORD", "Entrar": "Login",
    "① Factura Aportada": "① Uploaded Invoice", "② Revisión": "② Review", "③ Comparativa": "③ Comparison", "Ofertas DB": "Offers DB", "Configuración": "Configuration", "Salir": "Logout",
    "NOMBRE DEL ASESOR": "ADVISOR NAME", "FECHA DE LA PROPUESTA": "PROPOSAL DATE", "Subir factura": "Upload invoice", "Haz clic o arrastra archivos aquí": "Click or drag files here",
    "PDF o imágenes JPG/PNG · múltiples páginas permitido": "PDF or JPG/PNG images · multiple pages allowed", "✦ Extraer con IA": "✦ Extract with AI", "Cambiar archivos": "Change files",
    "Consumo Anual del CUPS": "Annual CUPS Consumption", "CONSUMO ANUAL TOTAL (kWh)": "TOTAL ANNUAL CONSUMPTION (kWh)", "POTENCIA CONTRATADA (kW)": "CONTRACTED POWER (kW)", "TARIFA DETECTADA": "DETECTED TARIFF",
    "Datos del cliente": "Customer data", "CLIENTE / RAZÓN SOCIAL": "CUSTOMER / COMPANY NAME", "COMERCIALIZADORA ACTUAL": "CURRENT SUPPLIER", "DIRECCIÓN": "ADDRESS", "CÓDIGO POSTAL": "POSTAL CODE", "TARIFA": "TARIFF",
    "Parámetros de facturación": "Billing parameters", "DÍAS FACTURADOS": "BILLED DAYS", "FECHA INICIO PERÍODO": "PERIOD START DATE", "TOTAL FACTURA (€) ⚠": "INVOICE TOTAL (€) ⚠",
    "IVA / IGIC (%)": "VAT / IGIC (%)", "IEE (%)": "IEE (%)", "IEE FACTURA ACTUAL (€)": "CURRENT INVOICE IEE (€)", "IVA FACTURA ACTUAL (€)": "CURRENT INVOICE VAT (€)", "DESCUENTO ENERGÍA ACTUAL (%)": "CURRENT ENERGY DISCOUNT (%)",
    "Períodos de precio": "Price periods", "Esta factura tiene 2 períodos de precio distintos": "This invoice has 2 different price periods",
    "Indica los días y precios de cada sub-período. La IA intentará extraerlos automáticamente.": "Indicate days and prices. AI will try to extract them automatically.",
    "DÍAS PERÍODO 1": "PERIOD 1 DAYS", "DÍAS PERÍODO 2": "PERIOD 2 DAYS", "€/kWh PERÍODO 1 (P1)": "€/kWh PERIOD 1 (P1)", "€/kWh PERÍODO 2 (P1)": "€/kWh PERIOD 2 (P1)",
    "Término de potencia — P1 a P6": "Power term — P1 to P6", "Término de energía — P1 a P6": "Energy term — P1 to P6", "kW": "kW", "IMPORTE (€)": "AMOUNT (€)", "kWh": "kWh", "€/kWh": "€/kWh",
    "Autoconsumo": "Self-consumption", "Esta factura tiene autoconsumo": "This invoice has self-consumption", "kWh GENERADOS / COMPENSADOS": "GENERATED / COMPENSATED kWh",
    "€/kWh PRECIO COMPENSACIÓN ACTUAL": "CURRENT €/kWh COMPENSATION PRICE", "TOTAL COMPENSACIÓN (€)": "TOTAL COMPENSATION (€)", "La compensación se calculará automáticamente: kWh × €/kWh": "Compensation calculated automatically: kWh × €/kWh",
    "Conceptos adicionales": "Additional concepts", "ENERGÍA REACTIVA (€)": "REACTIVE ENERGY (€)", "EXCESO POTENCIA (€)": "POWER EXCESS (€)", "ALQUILER EQUIPOS (€)": "EQUIPMENT RENTAL (€)",
    "BONO SOCIAL / FINANCIACIÓN (€)": "SOCIAL BONUS / FINANCING (€)", "SERVICIO / OTROS (€)": "SERVICE / OTHERS (€)", "solo factura actual": "only current invoice",
    "Otros conceptos sujetos a IEE": "Other concepts subject to IEE", "+ Añadir concepto": "+ Add concept", "Siguiente → Comparativa": "Next → Comparison", "← Volver": "← Back",
    "Facturación actual": "Current billing", "Ranking de ofertas": "Offers ranking", "Oferta seleccionada": "Selected offer", "📄 Generar PDF para comercial": "📄 Generate PDF for agent",
    "Base de Datos de Ofertas": "Offers Database", "Tarifas disponibles · se guardan en archivo local": "Available tariffs · saved in local file", "+ Nueva Oferta": "+ New Offer",
    "🔑 API Key Anthropic": "🔑 Anthropic API Key", "API KEY": "API KEY", "Guardar API Key": "Save API Key", "🌐 Idioma": "🌐 Language", "IDIOMA DE LA INTERFAZ": "INTERFACE LANGUAGE",
    "👤 Gestión de Usuarios": "👤 User Management", "+ Nuevo usuario": "+ New user", "Cancelar": "Cancel", "Guardar": "Save", "Guardar Oferta": "Save Offer",
    "Comisionado": "Commissions", "Comercializadoras": "Suppliers", "Añadir Tramo": "Add Tier", "Guardar Cambios": "Save Changes", "Eliminar Empresa": "Delete Company",
    "Escalado de Comisiones (Tramos)": "Commission Tiers (Tiers)", "Selecciona una comercializadora para configurar sus comissions.": "Select a supplier to configure its commissions.",
    "NOMBRE DE LA OFERTA": "OFFER NAME", "COMERCIALIZADORA": "SUPPLIER", "TIPO DE PRECIO": "PRICE TYPE", "PERMANENCIA": "COMMITMENT", "VALIDEZ (días)": "VALIDITY (days)",
    "Rango de aplicación": "Application range", "POT. MÍNIMA (kW)": "MIN POWER (kW)", "POT. MÁXIMA (kW)": "MAX POWER (kW)", "CONSUMO MÍN. (kWh/año)": "MIN CONSUMPTION (kWh/year)", "CONSUMO MÁX. (kWh/año)": "MAX CONSUMPTION (kWh/year)",
    "Comisión": "Commission", "TIPO DE COMISIÓN": "COMMISSION TYPE", "€ Fijo por contrato": "Fixed € per contract", "Por consumo (Coef. × kWh × FEE / 1000)": "By consumption",
    "COMISIÓN FIJA (€)": "FIXED COMMISSION (€)", "COEFICIENTE REPARTO (%)": "SPLIT COEFFICIENT (%)", "FEE (€/MWh)": "FEE (€/MWh)", "RESULTADO (se calcula automático)": "RESULT (calculated automatically)",
    "COMPENSACIÓN AUTOCONSUMO (€/kWh)": "SELF-CONSUMPTION COMP (€/kWh)", "DESCUENTO POTENCIA (%)": "POWER DISCOUNT (%)", "DESCUENTO ENERGÍA GLOBAL (%)": "GLOBAL ENERGY DISCOUNT (%)",
    "Discriminar dto. energía por periodo": "Discriminate energy discount by period", "Precios de potencia (€/kW/día)": "Power prices (€/kW/day)", "Precios de energía (€/kWh)": "Energy prices (€/kWh)",
    "NOMBRE": "NAME", "EMAIL": "EMAIL", "CONTRASEÑA": "PASSWORD", "(dejar vacío para no cambiar)": "(leave empty to keep)", "PERFIL": "PROFILE",
    "Admin": "Admin", "Comercial": "Agent", "Administración": "Administration",
    "Cargando...": "Loading...", "Selecciona una oferta": "Select an offer", "Credenciales incorrectas": "Invalid credentials",
    
    // PDF SPECIFIC
    "ESTUDIO COMPARATIVO ENERGÉTICO": "COMPARATIVE ENERGY STUDY", "Preparado el": "Prepared on", "Válido": "Valid for", "días": "days",
    "OFERTA": "OFFER", "TIPO": "TYPE", "FACTURACIÓN ACTUAL": "CURRENT BILLING", "NUEVA FACTURACIÓN": "NEW BILLING",
    "T. FIJO — POTENCIA": "FIXED TERM — POWER", "T. VARIABLE — ENERGÍA": "VARIABLE TERM — ENERGY", "OTROS CONCEPTOS": "OTHER CONCEPTS", "IMPUESTOS Y OTROS": "TAXES AND OTHERS",
    "TOTALES": "TOTALS", "TOTAL POTENCIA": "TOTAL POWER", "TOTAL ENERGÍA": "TOTAL ENERGY", "TOTAL": "TOTAL", "Base Imponible": "Taxable Base",
    "Compensación Autoconsumo": "Self-consumption Compensation", "Energía Reactiva": "Reactive Energy", "Alquiler Equipos": "Equipment Rental",
    "Financiación Bono Social": "Social Bonus Financing", "Servicios": "Services", "Imp. Electricidad (IEE)": "Electricity Tax (IEE)",
    "AHORRO ESTIMADO EN FACTURA": "ESTIMATED SAVINGS ON INVOICE", "Ahorro anual estimado": "Estimated annual savings", "año": "year", "€/año": "€/year",
    "Los precios de potencia y energía incluyen todos los PEAJES/ATR.": "Power and energy prices include all TOLLS/ATR.",
    "Cálculos de carácter informativo no vinculantes.": "Informative calculations, not binding.", "Fecha propuesta": "Proposal date", "Nombre del Asesor": "Advisor Name",
    "Sin permanencia": "No commitment", "PRECIO FIJO": "FIXED PRICE", "VARIABLE": "VARIABLE",
    "Tarifa": "Tariff", "PER.": "PER.", "€/kW·día": "€/kW·day", "DTO.": "DISC.", "IVA": "VAT"
  },
  ca: {
    "CORREO ELECTRÓNICO": "CORREU ELECTRÒNIC", "CONTRASEÑA": "CONTRASENYA", "Entrar": "Entrar",
    "① Factura Aportada": "① Factura Aportada", "② Revisión": "② Revisió", "③ Comparativa": "③ Comparativa", "Ofertas DB": "Ofertes BD", "Configuración": "Configuració", "Salir": "Sortir",
    "NOMBRE DEL ASESOR": "NOM DE L'ASSESSOR", "FECHA DE LA PROPUESTA": "DATA DE LA PROPOSTA", "Subir factura": "Pujar factura", "Haz clic o arrastra archivos aquí": "Fes clic o arrossega fitxers aquí",
    "PDF o imágenes JPG/PNG · múltiples páginas permitido": "PDF o imatges JPG/PNG · Múltiples pàgines permeses", "✦ Extraer con IA": "✦ Extreure amb IA", "Cambiar archivos": "Canviar fitxers",
    "Consumo Anual del CUPS": "Consum Anual del CUPS", "CONSUMO ANUAL TOTAL (kWh)": "CONSUM ANUAL TOTAL (kWh)", "POTENCIA CONTRATADA (kW)": "POTÈNCIA CONTRACTADA (kW)", "TARIFA DETECTADA": "TARIFA DETECTADA",
    "Datos del cliente": "Dades del client", "CLIENTE / RAZÓN SOCIAL": "CLIENT / RAÓ SOCIAL", "COMERCIALIZADORA ACTUAL": "COMERCIALITZADORA ACTUAL", "DIRECCIÓN": "ADREÇA", "CÓDIGO POSTAL": "CODI POSTAL", "TARIFA": "TARIFA",
    "Parámetros de facturación": "Paràmetres de facturació", "DÍAS FACTURADOS": "DIES FACTURATS", "FECHA INICIO PERÍODO": "DATA INICI PERÍODE", "TOTAL FACTURA (€) ⚠": "TOTAL FACTURA (€) ⚠",
    "IVA / IGIC (%)": "IVA / IGIC (%)", "IEE (%)": "IEE (%)", "IEE FACTURA ACTUAL (€)": "IEE FACTURA ACTUAL (€)", "IVA FACTURA ACTUAL (€)": "IVA FACTURA ACTUAL (€)", "DESCUENTO ENERGÍA ACTUAL (%)": "DESCOMPTE ENERGIA ACTUAL (%)",
    "Períodos de precio": "Períodes de preu", "Esta factura tiene 2 períodos de precio distintos": "Aquesta factura té 2 períodes de preu diferents",
    "Indica los días y precios de cada sub-período. La IA intentará extraerlos automáticamente.": "Indica els dies i preus. La IA intentarà extreure'ls automàticament.",
    "DÍAS PERÍODO 1": "DIES PERÍODE 1", "DÍAS PERÍODO 2": "DIES PERÍODE 2", "€/kWh PERÍODO 1 (P1)": "€/kWh PERÍODE 1 (P1)", "€/kWh PERÍODO 2 (P1)": "€/kWh PERÍODE 2 (P1)",
    "Término de potencia — P1 a P6": "Terme de potència — P1 a P6", "Término de energía — P1 a P6": "Terme d'energia — P1 a P6", "kW": "kW", "IMPORTE (€)": "IMPORT (€)", "kWh": "kWh", "€/kWh": "€/kWh",
    "Autoconsumo": "Autoconsum", "Esta factura tiene autoconsumo": "Aquesta factura té autoconsum", "kWh GENERADOS / COMPENSADOS": "kWh GENERATS / COMPENSATS",
    "€/kWh PRECIO COMPENSACIÓN ACTUAL": "€/kWh PREU COMPENSACIÓ ACTUAL", "TOTAL COMPENSACIÓN (€)": "TOTAL COMPENSACIÓ (€)", "La compensación se calculará automáticamente: kWh × €/kWh": "La compensació es calcularà automàticament: kWh × €/kWh",
    "Conceptos adicionales": "Conceptes addicionals", "ENERGÍA REACTIVA (€)": "ENERGIA REACTIVA (€)", "EXCESO POTENCIA (€)": "EXCÉS POTÈNCIA (€)", "ALQUILER EQUIPOS (€)": "LLOGUER EQUIPS (€)",
    "BONO SOCIAL / FINANCIACIÓN (€)": "BO SOCIAL / FINANÇAMENT (€)", "SERVICIO / OTROS (€)": "SERVEI / ALTRES (€)", "solo factura actual": "només factura actual",
    "Otros conceptos sujetos a IEE": "Altres conceptes subjectes a IEE", "+ Añadir concepto": "+ Afegir concepte", "Siguiente → Comparativa": "Següent → Comparativa", "← Volver": "← Tornar",
    "Facturación actual": "Facturació actual", "Ranking de ofertas": "Rànquing d'ofertes", "Oferta seleccionada": "Oferta seleccionada", "📄 Generar PDF para comercial": "📄 Generar PDF per a comercial",
    "Base de Datos de Ofertas": "Base de Dades d'Ofertes", "Tarifas disponibles · se guardan en archivo local": "Tarifes disponibles · Es guarden a l'arxiu local", "+ Nueva Oferta": "+ Nova Oferta",
    "🔑 API Key Anthropic": "🔑 API Key Anthropic", "API KEY": "API KEY", "Guardar API Key": "Desar API Key", "🌐 Idioma": "🌐 Idioma", "IDIOMA DE LA INTERFAZ": "IDIOMA DE LA INTERFÍCIE",
    "👤 Gestión de Usuarios": "👤 Gestió d'Usuaris", "+ Nuevo usuario": "+ Nou usuari", "Cancelar": "Cancel·lar", "Guardar": "Desar", "Guardar Oferta": "Desar Oferta",
    "Comisionado": "Comissionat", "Comercializadoras": "Comercialitzadores", "Añadir Tramo": "Afegir Tram", "Guardar Cambios": "Desar Canvis", "Eliminar Empresa": "Eliminar Empresa",
    "Escalado de Comisiones (Tramos)": "Escalat de Comissions (Trams)", "Selecciona una comercializadora para configurar sus comisiones.": "Selecciona una comercialitzadora per configurar les seves comissions.",
    "NOMBRE DE LA OFERTA": "NOM DE L'OFERTA", "COMERCIALIZADORA": "COMERCIALITZADORA", "TIPO DE PRECIO": "TIPUS DE PREU", "PERMANENCIA": "PERMANÈNCIA", "VALIDEZ (días)": "VALIDESA (dies)",
    "Rango de aplicación": "Rang d'aplicació", "POT. MÍNIMA (kW)": "POT. MÍNIMA (kW)", "POT. MÁXIMA (kW)": "POT. MÀXIMA (kW)", "CONSUMO MÍN. (kWh/año)": "CONSUM MÍN. (kWh/any)", "CONSUMO MÁX. (kWh/año)": "CONSUM MÀX. (kWh/any)",
    "Comisión": "Comissió", "TIPO DE COMISIÓN": "TIPUS DE COMISSIÓ", "€ Fijo por contrato": "€ Fix per contracte", "Por consumo (Coef. × kWh × FEE / 1000)": "Per consum",
    "COMISIÓN FIJA (€)": "COMISSIÓ FIXA (€)", "COEFICIENTE REPARTO (%)": "COEFICIENT REPARTIMENT (%)", "FEE (€/MWh)": "FEE (€/MWh)", "RESULTADO (se calcula automático)": "RESULTAT (es calcula automàticament)",
    "COMPENSACIÓN AUTOCONSUMO (€/kWh)": "COMPENSACIÓ AUTOCONSUM (€/kWh)", "DESCUENTO POTENCIA (%)": "DESCOMPTE POTÈNCIA (%)", "DESCUENTO ENERGÍA GLOBAL (%)": "DESCOMPTE ENERGIA GLOBAL (%)",
    "Discriminar dto. energía por periodo": "Discriminar dte. energia per període", "Precios de potencia (€/kW/día)": "Preus de potència (€/kW/dia)", "Precios de energía (€/kWh)": "Preus d'energia (€/kWh)",
    "NOMBRE": "NOM", "EMAIL": "EMAIL", "CONTRASEÑA": "CONTRASENYA", "(dejar vacío para no cambiar)": "(deixar buit per no canviar)", "PERFIL": "PERFIL",
    "Admin": "Admin", "Comercial": "Comercial", "Administración": "Administració",
    "Cargando...": "Carregant...", "Selecciona una oferta": "Selecciona una oferta", "Credenciales incorrectas": "Credencials incorrectes",

    // PDF SPECIFIC
    "ESTUDIO COMPARATIVO ENERGÉTICO": "ESTUDI COMPARATIU ENERGÈTIC", "Preparado el": "Preparat el", "Válido": "Vàlid per", "días": "dies",
    "OFERTA": "OFERTA", "TIPO": "TIPUS", "FACTURACIÓN ACTUAL": "FACTURACIÓ ACTUAL", "NUEVA FACTURACIÓN": "NOVA FACTURACIÓ",
    "T. FIJO — POTENCIA": "T. FIX — POTÈNCIA", "T. VARIABLE — ENERGÍA": "T. VARIABLE — ENERGIA", "OTROS CONCEPTOS": "ALTRES CONCEPTES", "IMPUESTOS Y OTROS": "IMPOSTOS I ALTRES",
    "TOTALES": "TOTALS", "TOTAL POTENCIA": "TOTAL POTÈNCIA", "TOTAL ENERGÍA": "TOTAL ENERGIA", "TOTAL": "TOTAL", "Base Imponible": "Base Imposable",
    "Compensación Autoconsumo": "Compensació Autoconsum", "Energía Reactiva": "Energia Reactiva", "Alquiler Equipos": "Lloguer Equips",
    "Financiación Bono Social": "Finançament Bo Social", "Servicios": "Serveis", "Imp. Electricidad (IEE)": "Imp. Electricitat (IEE)",
    "AHORRO ESTIMADO EN FACTURA": "ESTALVI ESTIMAT A LA FACTURA", "Ahorro anual estimado": "Estalvi anual estimat", "año": "any", "€/año": "€/any",
    "Los precios de potencia y energía incluyen todos los PEAJES/ATR.": "Els preus de potència i energia inclouen tots els PEATGES/ATR.",
    "Cálculos de carácter informativo no vinculantes.": "Càlculs de caràcter informatiu no vinculants.", "Fecha propuesta": "Data proposta", "Nombre del Asesor": "Nom de l'Assessor",
    "Sin permanencia": "Sense permanència", "PRECIO FIJO": "PREU FIX", "VARIABLE": "VARIABLE",
    "Tarifa": "Tarifa", "PER.": "PER.", "€/kW·día": "€/kW·dia", "DTO.": "DTE.", "IVA": "IVA"
  }
};

const _origTexts = new WeakMap();
function applyLang(root) {
  const lang = ST.config?.idioma || 'es';
  const dict = I18N[lang] || {};
  function walk(n) {
    if(n.nodeType === 3) {
      if(n.parentElement && n.parentElement.tagName === 'SCRIPT') return;
      if(n.parentElement && n.parentElement.tagName === 'STYLE') return;
      let txt = n.nodeValue.trim();
      if(txt && txt.length > 0) {
        if(!_origTexts.has(n)) _origTexts.set(n, txt);
        let orig = _origTexts.get(n);
        if(dict[orig]) n.nodeValue = n.nodeValue.replace(orig, dict[orig]);
        else if(lang==='es') n.nodeValue = n.nodeValue.replace(txt, orig);
      }
    } else if(n.nodeType === 1) {
      if(n.placeholder) {
        if(!_origTexts.has(n)) _origTexts.set(n, n.placeholder);
        let orig = _origTexts.get(n);
        n.placeholder = dict[orig] || (lang==='es'?orig:n.placeholder);
      }
      Array.from(n.childNodes).forEach(walk);
    }
  }
  walk(root || document.body);
}

function t(str) {
  const lang = ST.config?.idioma || 'es';
  return (I18N[lang] && I18N[lang][str]) ? I18N[lang][str] : str;
}

// ════════════════════════════════════════════
// ESTADO GLOBAL
// ════════════════════════════════════════════
const PS = ['P1','P2','P3','P4','P5','P6'];
const $ = id => document.getElementById(id);
const n = v => parseFloat(v)||0;
const clean = s => (s||'').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();

let ST = {
  user: null,           // usuario logueado
  config: {},
  files: [],
  ofertas: [],
  comisiones: [], // Centralized commissions
  usuarios: [],
  sel: null,
  selCom: null, // Selected company in Comisionado
  editOfrId: null,
  editUserId: null,
  _res: []
};

// ════════════════════════════════════════════
// AUTENTICACIÓN
// ════════════════════════════════════════════
async function doLogin(){
  const email = $('l_email').value.trim();
  const pass  = $('l_pass').value;
  if(!email||!pass) return;
  try {
    const r = await fetch('/api/login', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({email, password: pass})
    });
    const d = await r.json();
    if(d.ok){
      ST.user = d.user;
      $('l_err').style.display='none';
      $('l_pass').value='';
      initApp();
    } else {
      $('l_err').style.display='block';
      $('l_err').textContent = d.error||'Credenciales incorrectas';
    }
  } catch(e){ $('l_err').style.display='block'; $('l_err').textContent='Error de conexión'; }
}

function doLogout(){
  ST.user=null; ST.sel=null;
  $('loginScreen').style.display='flex';
  $('shell').style.display='none';
}

// ════════════════════════════════════════════
// INIT APP
// ════════════════════════════════════════════
async function initApp(){
  $('loginScreen').style.display='none';
  $('shell').style.display='flex';

  // User info in topbar
  $('ui_nombre').textContent = ST.user.nombre;
  $('ui_role').textContent = ST.user.role==='admin' ? 'Admin' : 'Comercial';

  // Role-based tab visibility
  const isAdmin = ST.user.role === 'admin';
  $('tab-ofr').style.display = isAdmin ? '' : 'none';
  $('tab-com').style.display = isAdmin ? '' : 'none';

  // Load config, offers, users, comisiones
  await Promise.all([loadConfig(), loadOfertas(), loadUsuarios(), loadComisiones()]);

  // Populate config UI
  $('cfg_apikey').value = '';
  $('cfg_apikey').placeholder = ST.config.has_api_key ? '*** API Key guardada ***' : 'sk-ant-...';
  $('cfg_idioma').value = ST.config.idioma||'es';

  // Admin sees cfg-api, comercial doesn't
  $('cfg-api').style.display = isAdmin ? '' : 'none';
  $('cfg-users-addbar').style.display = isAdmin ? '' : 'none';

  // Restore asesor
  $('g_asesor').value = localStorage.getItem('el_asesor')||'';
  const today = new Date().toISOString().split('T')[0];
  $('g_fecha').value = today;

  buildTbls();
  renderUsersTable();
  go('fac');
  applyLang();
}

// ════════════════════════════════════════════
// API CALLS
// ════════════════════════════════════════════
async function loadConfig(){
  try{ const r=await fetch('/api/config'); ST.config=await r.json(); } catch(e){}
}
async function saveConfig(){
  const newKey = $('cfg_apikey').value.trim();
  if(newKey) ST.config.api_key = newKey;
  ST.config.idioma  = $('cfg_idioma').value;
  await fetch('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.config)});
  if(newKey) ST.config.has_api_key = true;
  sb('Configuración guardada ✓','ok');
  applyLang();
}
async function loadOfertas(){
  try{ const r=await fetch('/api/ofertas'); ST.ofertas=await r.json(); updCnt(); } catch(e){}
}
async function saveOfertasToServer(){
  await fetch('/api/ofertas',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.ofertas)});
}
async function loadUsuarios(){
  try{ const r=await fetch('/api/usuarios'); ST.usuarios=await r.json(); } catch(e){}
}
async function saveUsuariosToServer(){
  await fetch('/api/usuarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.usuarios)});
}

async function loadComisiones(){
  try{ const r=await fetch('/api/comisiones'); ST.comisiones=await r.json(); } catch(e){}
}
async function saveComs(){
  if(!ST.selCom) return;
  const tramos = Array.from($('comTramosT').querySelectorAll('tr')).map(tr => {
    const inp = tr.querySelectorAll('input, select');
    return {
      p_min: n(inp[0].value), p_max: n(inp[1].value),
      c_min: n(inp[2].value), c_max: n(inp[3].value),
      filtro: inp[4].value.trim(),
      valor: n(inp[5].value), tipo: inp[6].value
    };
  });
  const idx = ST.comisiones.findIndex(c => c.id === ST.selCom.id);
  if(idx !== -1) ST.comisiones[idx].tramos = tramos;
  
  await fetch('/api/comisiones',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.comisiones)});
  sb('Comisiones guardadas ✓','ok');
  renderComList();
}

function renderComList(){
  const el = $('comList');
  if(!ST.comisiones.length){ el.innerHTML = '<div style="color:var(--t3);font-size:11px;padding:10px">No hay empresas configuradas.</div>'; return; }
  el.innerHTML = ST.comisiones.map(c => `
    <div class="com-item ${ST.selCom?.id === c.id ? 'active' : ''}" onclick="openComCo('${c.id}')">
      ${c.comercializadora}
      <span style="font-size:9px;opacity:0.6">${c.tramos?.length || 0} tramos</span>
    </div>
  `).join('');
}

function addComCo(){
  const name = prompt(t('Nombre de la Comercializadora:'));
  if(!name) return;
  const id = 'com_' + Date.now();
  ST.comisiones.push({ id, comercializadora: name.toUpperCase(), tramos: [] });
  saveComsToServer(); // Save immediately to prevent loss
  renderComList();
  openComCo(id);
}

async function saveComsToServer(){
  await fetch('/api/comisiones',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.comisiones)});
}

async function delComCo(){
  if(!ST.selCom || !confirm('¿Eliminar esta empresa y todas sus reglas?')) return;
  ST.comisiones = ST.comisiones.filter(c => c.id !== ST.selCom.id);
  ST.selCom = null;
  await fetch('/api/comisiones',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.comisiones)});
  renderComList();
  $('comEditor').style.display = 'none';
  $('comEditorEmpty').style.display = 'flex';
}

function openComCo(id){
  const c = ST.comisiones.find(x => x.id === id);
  if(!c) return;
  ST.selCom = c;
  $('comEditorEmpty').style.display = 'none';
  $('comEditor').style.display = 'block';
  $('comCoName').textContent = c.comercializadora;
  $('comTramosT').innerHTML = '';
  if(c.tramos) c.tramos.forEach(t => addComTramo(t));
  renderComList();
}

function addComTramo(t){
  t = t || { p_min:0, p_max:9999, c_min:0, c_max:9999999, filtro:'', valor:0, tipo:'fijo' };
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td><input type="number" step="0.01" value="${t.p_min}" placeholder="0"></td>
    <td><input type="number" step="0.01" value="${t.p_max}" placeholder="9999"></td>
    <td><input type="number" step="1" value="${t.c_min}" placeholder="0"></td>
    <td><input type="number" step="1" value="${t.c_max}" placeholder="99999"></td>
    <td><input type="text" placeholder="Ej: Supra" value="${t.filtro || ''}" style="width:100%; min-width:120px"></td>
    <td><input type="number" step="0.01" value="${t.valor}" placeholder="0.00" style="font-weight:700; color:var(--acc)"></td>
    <td>
      <select>
        <option value="fijo" ${t.tipo==='fijo'?'selected':''}>Fijo (€)</option>
        <option value="variable" ${t.tipo==='variable'?'selected':''}>Variable (€/MWh)</option>
      </select>
    </td>
    <td><button class="btn btn-d" onclick="this.closest('tr').remove()">✕</button></td>
  `;
  $('comTramosT').appendChild(tr);
}

// ════════════════════════════════════════════
// NAV
// ════════════════════════════════════════════
function updCnt(){ $('vcnt') && ($('vcnt').textContent = ST.ofertas.length+' ofertas'); }
function go(id){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('on'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
  $('p-'+id).classList.add('on');
  $('tab-'+id)?.classList.add('on');
  if(id==='cmp'){ loadOfertas().then(()=>renderCmp()); }
  if(id==='ofr'){ loadOfertas().then(()=>renderOfrList()); }
  if(id==='com'){ renderComList(); }
  if(id==='cfg'){ renderUsersTable(); }
}

// ════════════════════════════════════════════
// STATUS BAR
// ════════════════════════════════════════════
function sb(msg, type){
  const el=$('sb'); el.style.display='flex'; el.className='sb-bar '+type;
  el.innerHTML = type==='load'?'<div class="spin"></div><span>'+msg+'</span>':'<span>'+msg+'</span>';
  if(type!=='load') setTimeout(()=>el.style.display='none',4500);
}

// ════════════════════════════════════════════
// TABLES
// ════════════════════════════════════════════
let potIdSeq=0, enIdSeq=0, lecIdSeq=0;
function buildTbls(){
  $('potT').innerHTML=''; $('enT').innerHTML=''; $('lecT').innerHTML='';
  PS.forEach(p=>{ addPotL(p); addEnL(p); addLecL(p); });
}
function addPotL(per){
  const p=per||$('addPotSel').value; const id=potIdSeq++;
  const tr=document.createElement('tr'); tr.className='pot-row'; tr.dataset.per=p;
  tr.innerHTML='<td class="lbl">'+p+'</td><td><input type="number" id="pk_'+id+'" class="pk_in" step=".001" value="0"></td><td><input type="number" id="pi_'+id+'" class="pi_in" step=".01" value="0"></td><td><button class="btn btn-d" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  $('potT').appendChild(tr);
}
function addEnL(per){
  const p=per||$('addEnSel').value; const id=enIdSeq++;
  const tr=document.createElement('tr'); tr.className='en-row'; tr.dataset.per=p;
  tr.innerHTML='<td class="lbl">'+p+'</td><td><input type="number" id="ek_'+id+'" class="ek_in" step=".001" value="0"></td><td><input type="number" id="ep_'+id+'" class="ep_in" step=".000001" value="0"></td><td><button class="btn btn-d" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  $('enT').appendChild(tr);
}
function addLecL(per){
  const p=per||$('addLecSel').value; const id=lecIdSeq++;
  const tr=document.createElement('tr'); tr.className='lec-row'; tr.dataset.per=p;
  tr.innerHTML='<td class="lbl">'+p+'</td><td><input type="number" id="lk_'+id+'" class="lk_in" step=".001" value="0"></td><td><button class="btn btn-d" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  $('lecT').appendChild(tr);
}

function updTar(){
  const v = n($('f_pot').value);
  const currentTar = $('f_tar').value;
  let t = v<=15?'2.0TD':'3.0TD';
  // Solo sugerimos 6.1TD si la potencia es muy alta (>150kW) o si ya estaba seleccionada
  if(v > 150 && currentTar !== '3.0TD') t = '6.1TD';
  
  $('f_tar').value=t;
  $('f_tar_cups').value=t;
  $('tarTag').textContent=t;
  $('potHint').style.display = t!=='2.0TD'?'block':'none';
  $('f_pot_cups').value = v||'';
}

function syncTar(v){
  $('f_tar').value=v;
  $('f_tar_cups').value=v;
  $('tarTag').textContent=v;
  $('potHint').style.display = v!=='2.0TD'?'block':'none';
}

function syncPot(){
  const v=n($('f_pot_cups').value);
  $('f_pot').value=v;
  updTar();
}

function togDosPeriodos(){
  const c=$('f_dos_periodos').checked;
  $('dosPeriodosInfo').style.display=c?'block':'none';
  $('addPotBtn').style.display=c?'flex':'none';
  $('addEnBtn').style.display=c?'flex':'none';
}
function togAutocon(){
  const c=$('f_tiene_autocon').checked;
  $('autoconFields').style.display=c?'block':'none';
}

// Auto-calc compensacion total
document.addEventListener('input', function(e){
  if(e.target.id==='f_aut_kwh'||e.target.id==='f_aut_precio'){
    const kwh=n($('f_aut_kwh').value), precio=n($('f_aut_precio').value);
    $('f_aut_total').value=(kwh*precio).toFixed(2);
  }
  if(e.target.id==='g_asesor') localStorage.setItem('el_asesor',e.target.value);
});

// ════════════════════════════════════════════
// FILE UPLOAD
// ════════════════════════════════════════════
function onFiles(flist){
  const files=Array.from(flist); if(!files.length) return;
  ST.files=[]; $('chips').innerHTML=''; let loaded=0;
  files.forEach(function(file){
    const r=new FileReader();
    r.onload=function(e){
      ST.files.push({data:e.target.result.split(',')[1], type:file.type, name:file.name, src:e.target.result});
      $('chips').innerHTML+='<span class="chip">'+(file.type.includes('pdf')?'📄':'🖼️')+' '+file.name+'</span>';
      if(++loaded===files.length){
        const img=ST.files.find(function(f){return !f.type.includes('pdf');});
        if(img){$('prevImg').src=img.src;$('prevImg').style.display='block';}
        else $('prevImg').style.display='none';
        $('prevSec').style.display='block';
        $('upzone').style.borderColor='var(--acc)';
        $('upSub').textContent=loaded+' archivo'+(loaded>1?'s':'')+' listo'+(loaded>1?'s':'')+' para analizar';
      }
    };
    r.readAsDataURL(file);
  });
}
function resetUp(){
  ST.files=[];$('prevSec').style.display='none';$('chips').innerHTML='';
  $('upzone').style.borderColor='';$('fInput').value='';
  $('upSub').textContent='PDF o imágenes JPG/PNG · múltiples páginas permitido';
}
const uz=$('upzone');
uz.addEventListener('dragover',function(e){e.preventDefault();uz.style.borderColor='var(--acc)';});
uz.addEventListener('dragleave',function(){uz.style.borderColor='';});
uz.addEventListener('drop',function(e){e.preventDefault();uz.style.borderColor='';onFiles(e.dataTransfer.files);});

// ════════════════════════════════════════════
// IA EXTRACTION
// ════════════════════════════════════════════
const normMime=function(t){
  if(!t||t.includes('pdf')) return 'application/pdf';
  if(t.includes('png')) return 'image/png';
  if(t.includes('gif')) return 'image/gif';
  if(t.includes('webp')) return 'image/webp';
  return 'image/jpeg';
};

async function extract(){
  const hasKey = ST.config.has_api_key || !!ST.config.api_key;
  if(!hasKey){sb('Configura la API Key en Configuración primero','err');return;}
  if(!ST.files.length){sb('Sube al menos un archivo','err');return;}
  $('btnEx').disabled=true; sb('Analizando factura con IA…','load');

  const prompt='Eres experto en facturas eléctricas españolas. Extrae TODOS los datos. Responde SOLO JSON válido sin markdown:\n'
  +'{"cliente":"","cups":"","comercializadora":"","direccion":"","cp":"","tarifa":"","potencia_kw":0,"dias":0,"fecha_inicio":"YYYY-MM-DD",'
  +'"total_factura":0,"iva_pct":21,"iee_pct":5.1126963,"iee_act":0,"iva_act":0,"dto_energia_act_pct":0,'
  +'"tiene_autoconsumo":false,"autoconsumo_kwh":0,"autoconsumo_precio_kwh":0,"autoconsumo_total":0,'
  +'"tiene_multiples_periodos":false,'
  +'"potencia":[{"per":"P1","kw":0,"importe":0},{"per":"P2","kw":0,"importe":0}],'
  +'"energia":[{"per":"P1","kwh":0,"precio":0},{"per":"P2","kwh":0,"precio":0}],'
  +'"lecturas_energia":[{"per":"P1","kwh":0},{"per":"P2","kwh":0},{"per":"P3","kwh":0}],'
  +'"reactiva":0,"exceso_potencia":0,"alquiler_equipos":0,"bono_social":0,"servicio":0,'
  +'"iee_extras":[{"nombre":"","importe":0}],'
  +'"confianza":{"total_factura":"alta","potencia":"alta","energia":"alta"}}\n'
  +'REGLAS CRÍTICAS:\n'
  +'1. Busca explícitamente el nombre de la "Tarifa" o "Peaje de acceso" (ej: 2.0TD, 3.0TD, 6.1TD) y devuélvelo en el campo "tarifa".\n'
  +'2. El array "energia" representa EXACTAMENTE las líneas de facturación tal como aparecen impresas en la factura (puede ser 1 sola línea de tarifa plana, o varias por período). Extrae fielmente esos importes y precios.\n'
  +'3. El array "lecturas_energia" es INDEPENDIENTE: busca la sección "Lecturas" / "Información de Consumo" / "Detalle de consumo" del documento y extrae el desglose real de kWh por período P1, P2, P3... Si no existen lecturas desglosadas, copia los kWh del array energia agrupados por período. NUNCA dejes lecturas_energia vacío si hay datos de consumo en el documento.\n'
  +'4. Si hay varios sub-períodos de precio, "tiene_multiples_periodos"=true y devuelve líneas extra en "energia".\n'
  +'5. Valores inexistentes=0 o "".';

  const uc=[];
  ST.files.forEach(function(f){
    const m=normMime(f.type);
    uc.push(m==='application/pdf'
      ?{type:'document',source:{type:'base64',media_type:'application/pdf',data:f.data}}
      :{type:'image',source:{type:'base64',media_type:m,data:f.data}});
  });
  const note=ST.files.length>1?'Son '+ST.files.length+' páginas de la MISMA factura. Devuelve UN SOLO JSON consolidado. ':'';
  uc.push({type:'text',text:note+prompt});

  try{
    const resp=await fetch('/api/claude',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({messages:[{role:'user',content:uc}]})
    });
    const d=await resp.json();
    if(d.error) throw new Error(d.error);
    const ex=JSON.parse(d.text.replace(/```json|```/g,'').trim());
    fillForm(ex);
    sb('Extracción completada ✓ — Revisa los datos en "Revisión"','ok');
    go('rev');
  }catch(e){
    sb('Error: '+e.message,'err');
  }finally{
    $('btnEx').disabled=false;
  }
}

// ════════════════════════════════════════════
// FILL FORM
// ════════════════════════════════════════════
function fillForm(d){
  const set=function(id,v,c){
    const el=$(id); if(!el) return;
    el.value=v||'';
    el.classList.remove('ai','unc');
    if(v) el.classList.add((c==='baja'||c==='media')?'unc':'ai');
  };
  set('f_cli',d.cliente); set('f_cups',d.cups); set('f_com',d.comercializadora);
  set('f_dir',d.direccion); set('f_cp',d.cp); set('f_pot',d.potencia_kw);
  set('f_dias',d.dias); set('f_fi',d.fecha_inicio);
  set('f_tot',d.total_factura,d.confianza?.total_factura);
  set('f_iva',d.iva_pct); set('f_iee',d.iee_pct);
  set('f_iee_act',d.iee_act); set('f_iva_act',d.iva_act);
  set('f_dto_en_act',d.dto_energia_act_pct);
  set('f_rea',d.reactiva); set('f_exc',d.exceso_potencia);
  set('f_alq',d.alquiler_equipos); set('f_bon',d.bono_social); set('f_ser',d.servicio);
  // Autoconsumo
  if(d.tiene_autoconsumo){
    $('f_tiene_autocon').checked=true; togAutocon();
    set('f_aut_kwh',d.autoconsumo_kwh,'alta');
    set('f_aut_precio',d.autoconsumo_precio_kwh,'alta');
    set('f_aut_total',d.autoconsumo_total,'alta');
  }
  // Múltiples periodos
  if(d.tiene_multiples_periodos){
    $('f_dos_periodos').checked=true; togDosPeriodos();
  } else {
    $('f_dos_periodos').checked=false; togDosPeriodos();
  }
  // Periodos
  $('potT').innerHTML=''; $('enT').innerHTML='';
  let maxKw=0;
  
  const potArr = Array.isArray(d.potencia) ? d.potencia : PS.map(p=>({per:p,...(d.potencia?.[p]||{})}));
  potArr.forEach(p => {
    addPotL(p.per); const id = potIdSeq - 1;
    const kwEl=$('pk_'+id), piEl=$('pi_'+id);
    kwEl.value = p.kw||0; piEl.value = p.importe||0;
    if(n(p.kw)>maxKw) maxKw=n(p.kw);
    const cp=d.confianza?.potencia;
    if(p.kw) kwEl.classList.add(cp==='baja'?'unc':'ai');
    if(p.importe) piEl.classList.add(cp==='baja'?'unc':'ai');
  });

  const enArr = Array.isArray(d.energia) ? d.energia : PS.map(p=>({per:p,...(d.energia?.[p]||{})}));
  enArr.forEach(e => {
    addEnL(e.per); const id = enIdSeq - 1;
    const khEl=$('ek_'+id), prEl=$('ep_'+id);
    khEl.value = e.kwh||0; prEl.value = e.precio||0;
    const ce=d.confianza?.energia;
    if(e.kwh) khEl.classList.add(ce==='baja'?'unc':'ai');
    if(e.precio) prEl.classList.add(ce==='baja'?'unc':'ai');
  });

  // Lecturas reales para simulación (campo separado de la IA)
  $('lecT').innerHTML=''; lecIdSeq=0;
  const lecArr = Array.isArray(d.lecturas_energia) ? d.lecturas_energia : [];
  const hasLec = lecArr.some(l=>n(l.kwh)>0);
  if(hasLec){
    lecArr.forEach(l=>{
      if(n(l.kwh)>0){
        addLecL(l.per); const id=lecIdSeq-1;
        const lkEl=$('lk_'+id);
        lkEl.value=l.kwh||0;
        if(l.kwh) lkEl.classList.add('ai');
      }
    });
  } else {
    // Fallback: si la IA no devolvió lecturas, agrupa los kWh de energía por periodo
    PS.forEach(p=>{
      const total=enArr.filter(e=>e.per===p).reduce((s,e)=>s+n(e.kwh),0);
      addLecL(p); const id=lecIdSeq-1;
      $('lk_'+id).value=total>0?total:0;
    });
  }

  // Asignar potencia contratada a la potencia máxima detectada
  if(maxKw>0) d.potencia_kw = maxKw;
  // Sync potencia a factura aportada
  $('f_pot_cups').value=d.potencia_kw||'';
  
  // Decidir Tarifa: Prioridad a lo extraído por IA si es válido
  let tarFinal = '';
  if(d.tarifa && ['2.0TD','3.0TD','6.1TD'].includes(d.tarifa.toUpperCase())) {
     tarFinal = d.tarifa.toUpperCase();
  } else {
     const tv=n(d.potencia_kw);
     tarFinal = tv<=15?'2.0TD':'3.0TD'; // Default conservative
     if(tv > 150) tarFinal = '6.1TD'; 
  }
  
  $('f_tar').value=tarFinal;
  $('f_tar_cups').value=tarFinal;
  updTar();
  // IEE extras
  clearIeeExtras();
  if(d.iee_extras&&d.iee_extras.length){
    d.iee_extras.forEach(function(e){if(e.nombre&&e.importe) addIeeExtra(e.nombre,e.importe,false);});
  }
}

// ════════════════════════════════════════════
// GET FORM DATA
// ════════════════════════════════════════════
let ieeExtraCount=0;
function addIeeExtra(nombre,importe,mantiene){
  nombre=nombre||''; importe=importe||0; mantiene=mantiene||false;
  const id='iee_'+Date.now()+'_'+(ieeExtraCount++);
  const div=document.createElement('div');
  div.id=id; div.style.cssText='display:grid;grid-template-columns:1fr 110px auto auto;gap:8px;align-items:center;margin-bottom:7px';
  const i1=document.createElement('input'); i1.type='text'; i1.placeholder='Ej: Ajust Restriccions / SA de REE'; i1.value=nombre; i1.style.cssText='background:var(--bg);border:1px solid var(--b1);border-radius:6px;padding:7px 10px;color:var(--tx);font-family:monospace;font-size:12px;width:100%';
  const i2=document.createElement('input'); i2.type='number'; i2.step='.01'; i2.placeholder='€'; i2.value=importe||''; i2.style.cssText='background:var(--bg);border:1px solid var(--b1);border-radius:6px;padding:7px 10px;color:var(--tx);font-family:monospace;font-size:12px;text-align:right;width:100%';
  const lbl=document.createElement('label'); lbl.style.cssText='display:flex;align-items:center;gap:5px;font-size:10px;color:var(--t2);cursor:pointer;white-space:nowrap';
  const chk=document.createElement('input'); chk.type='checkbox'; chk.checked=mantiene; chk.style.accentColor='var(--acc)';
  lbl.appendChild(chk); lbl.appendChild(document.createTextNode(' En nueva'));
  const btn=document.createElement('button'); btn.className='btn btn-d'; btn.textContent='✕'; btn.onclick=function(){document.getElementById(id).remove();};
  div.appendChild(i1); div.appendChild(i2); div.appendChild(lbl); div.appendChild(btn);
  const container = $('ieeExtras');
  if(container) container.appendChild(div);
  else console.warn("Contenedor 'ieeExtras' no encontrado.");
}
function getIeeExtras(){
  return Array.from($('ieeExtras').querySelectorAll('div[id^="iee_"]')).map(function(row){
    const inp=row.querySelectorAll('input');
    return {nombre:inp[0].value, importe:n(inp[1].value), mantiene:inp[2].checked};
  }).filter(function(r){return r.importe>0;});
}
function clearIeeExtras(){$('ieeExtras').innerHTML=''; ieeExtraCount=0;}

function getForm(){
  const potArr=[], enArr=[], lecArr=[];
  document.querySelectorAll('.pot-row').forEach(tr=>{
    potArr.push({per:tr.dataset.per, kw:n(tr.querySelector('.pk_in').value), importe:n(tr.querySelector('.pi_in').value)});
  });
  document.querySelectorAll('.en-row').forEach(tr=>{
    enArr.push({per:tr.dataset.per, kwh:n(tr.querySelector('.ek_in').value), precio:n(tr.querySelector('.ep_in').value)});
  });
  document.querySelectorAll('.lec-row').forEach(tr=>{
    lecArr.push({per:tr.dataset.per, kwh:n(tr.querySelector('.lk_in').value)});
  });
  // Determinar si hay lecturas reales con valores > 0
  const hasLecturas = lecArr.some(l=>l.kwh>0);
  // Si no hay lecturas con valor, fallback a usar los kWh de energía agrupados por periodo
  const lecByPer = {};
  PS.forEach(p=>{ lecByPer[p]=0; });
  if(hasLecturas){
    lecArr.forEach(l=>{ if(lecByPer[l.per]!==undefined) lecByPer[l.per]+=l.kwh; });
  } else {
    enArr.forEach(l=>{ if(lecByPer[l.per]!==undefined) lecByPer[l.per]+=l.kwh; });
  }
  const tieneAuto=$('f_tiene_autocon').checked;
  const autKwh=tieneAuto?n($('f_aut_kwh').value):0;
  const autPrecio=tieneAuto?n($('f_aut_precio').value):0;
  return {
    cliente:$('f_cli').value, cups:$('f_cups').value,
    comercializadora:$('f_com').value, direccion:$('f_dir').value, cp:$('f_cp').value,
    potencia_kw:n($('f_pot').value), dias:n($('f_dias').value),
    fecha_inicio:$('f_fi').value, total_factura:n($('f_tot').value),
    iva_pct:n($('f_iva').value)||21, iee_pct:n($('f_iee').value)||5.1126963,
    iee_act:n($('f_iee_act').value), iva_act:n($('f_iva_act').value),
    dto_en_act_pct:n($('f_dto_en_act').value),
    reactiva:n($('f_rea').value), exceso_potencia:n($('f_exc').value),
    alquiler_equipos:n($('f_alq').value), bono_social:n($('f_bon').value), servicio:n($('f_ser').value),
    tarifa:$('f_tar').value||'2.0TD',
    consumo_anual:n($('f_consumo_anual').value),
    tiene_autoconsumo:tieneAuto, autoconsumo_kwh:autKwh, autoconsumo_precio_kwh:autPrecio,
    tiene_multiples_periodos:$('f_dos_periodos').checked,
    pot_p:potArr, en_p:enArr,
    lec_p:lecArr, lec_by_per:lecByPer, has_lecturas:hasLecturas,
    iee_extras:getIeeExtras()
  };
}

// ════════════════════════════════════════════
// CALCULOS
// ════════════════════════════════════════════
function calcComision(oferta, d){
  const pot = d.potencia_kw || 0;
  const consumo = d.consumo_anual || 0;
  
  // Buscar regla centralizada para esta comercializadora
  const slug = clean(oferta.comercializadora);
  const regla = ST.comisiones.find(c => clean(c.comercializadora) === slug);
  
  if(regla && regla.tramos && regla.tramos.length){
    const ofrName = clean(oferta.nombre);
    // Buscar el tramo correspondiente
    const tramo = regla.tramos.find(t => {
      const matchPot = pot >= t.p_min && pot < t.p_max;
      const matchCons = consumo >= t.c_min && consumo < t.c_max;
      const matchName = !t.filtro || ofrName.includes(clean(t.filtro));
      return matchPot && matchCons && matchName;
    });
    if(tramo){
      if(tramo.tipo === 'variable') return tramo.valor * (consumo / 1000);
      return tramo.valor * (d.dias/365); 
    }
  }

  // Fallback a los campos de la oferta (Retrocompatibilidad)
  if(oferta.tipo_comision==='consumo' || oferta.tipo_comision==='kwh'){
    const val = oferta.comision || 0;
    if(oferta.tipo_comision==='consumo'){
        const coef=(oferta.coef_reparto||0)/100;
        const fee=oferta.fee_mwh||0;
        return coef * consumo * fee / 1000;
    }
    return consumo * val;
  }
  return (oferta.comision||0) * (d.dias/365);
}

function calcOfr(d, o){
  // Potencia: agrupar máximo kW por periodo
  const potByPer={};
  PS.forEach(p=>{potByPer[p]={kw:0}});
  d.pot_p.forEach(l=>{ if(potByPer[l.per] && l.kw>potByPer[l.per].kw) potByPer[l.per].kw=l.kw; });

  // Energía para la NUEVA OFERTA: usar lecturas reales si existen, si no usar en_p
  const simByPer = d.lec_by_per || {};
  const totalKwh = PS.reduce((s,p)=>s+(simByPer[p]||0), 0);

  let tPot=0;
  PS.forEach(p=>{
    // Para la nueva oferta, siempre usamos la potencia contratada global (d.potencia_kw).
    // Cada periodo solo contribuye si la oferta tiene precio para ese periodo (pp>0).
    // ELIMINADO: el fallback P3->pp_p2 causaba doble conteo en 2.0TD.
    const ppNva=o['pp_'+p.toLowerCase()]||0;
    if(ppNva>0) tPot+=d.potencia_kw*ppNva*d.dias;
  });
  tPot*=(1-(o.dto_potencia||0)/100);
  
  let tEn=0;
  PS.forEach((p,i)=>{
    const kwh=simByPer[p]||0;
    const precio=o['ep_'+p.toLowerCase()]||0;
    const dto=o.dto_energia_por_periodo?(o['dto_e_p'+(i+1)]||0)/100:(o.dto_energia_global||0)/100;
    tEn+=kwh*precio*(1-dto);
  });
  // Autoconsumo en nueva oferta
  const compNva=d.tiene_autoconsumo?(d.autoconsumo_kwh||0)*(o.compensacion||0):0;
  const rea=d.reactiva, exc=d.exceso_potencia, alq=d.alquiler_equipos, bon=d.bono_social;
  const extrasIEE=(d.iee_extras||[]).filter(function(e){return e.mantiene;}).reduce(function(s,e){return s+e.importe;},0);
  const baseIEE=tPot+tEn+rea+exc+bon+extrasIEE-compNva;
  const iee=baseIEE*(d.iee_pct/100);
  const baseIVA=baseIEE+iee+alq;
  const iva=baseIVA*(d.iva_pct/100);
  const total=baseIVA+iva;
  const comision=calcComision(o,d);
  return {tPot,tEn,compNva,iee,baseIEE,baseIVA,iva,total,comision,totalKwh};
}

function ofertaMatchesFact(o, d){
  const cAct = clean(d.comercializadora);
  const cOfr = clean(o.comercializadora);

  // 1. Auto-exclusión: No ofrecer la misma compañía que ya tiene
  if(cAct && cOfr && cAct === cOfr) return false;

  // 2. Iberdrola <-> Niba (Exclusión mutua)
  const isIbe = cAct.includes('iberdrola') || cOfr.includes('iberdrola');
  const isNib = cAct.includes('niba') || cOfr.includes('niba');
  if(isIbe && isNib) return false;

  // 3. Energía XXI <-> Endesa (Exclusión mutua)
  const isExxi = cAct.includes('energia xxi') || cOfr.includes('energia xxi');
  const isEnd = cAct.includes('endesa') || cOfr.includes('endesa');
  if(isExxi && isEnd) return false;

  // Tarifa
  if(o.tarifa!=='todas' && o.tarifa!==d.tarifa) return false;
  // Potencia
  const pot=d.potencia_kw;
  if(pot<(o.pot_min||0) || pot>(o.pot_max||9999)) return false;
  // Consumo anual
  const ca=d.consumo_anual||0;
  if(ca>0){
    if(ca<(o.consumo_min||0) || ca>(o.consumo_max||99999999)) return false;
  }
  return true;
}

// ════════════════════════════════════════════
// COMPARATIVA
// ════════════════════════════════════════════
function renderCmp(){
  const d=getForm();
  const tPotAct = d.pot_p.reduce((s,l)=>s+l.importe, 0);
  const tEnAct = d.en_p.reduce((s,l)=>s+(l.kwh*l.precio), 0);
  const autAct=d.tiene_autoconsumo?(d.autoconsumo_kwh||0)*(d.autoconsumo_precio_kwh||0):0;
  
  const servSum = d.servicio || 0;
  const baseIVAAct = (d.total_factura - d.iva_act) + servSum;
  const ivaActCalc = d.iva_act + (servSum * (d.iva_pct/100));
  const calcTotalAct = baseIVAAct + ivaActCalc;

  $('actCard').innerHTML='<div class="ct">📋 '+( d.comercializadora||'Comercializadora actual' )+'</div>'
    +'<div class="trow"><span class="trow-l">Potencia</span><span>'+tPotAct.toFixed(2)+' €</span></div>'
    +'<div class="trow"><span class="trow-l">Energía</span><span>'+tEnAct.toFixed(2)+' €</span></div>'
    +(d.tiene_autoconsumo?'<div class="trow"><span class="trow-l">Compensación autoconsumo</span><span style="color:var(--ok)">-'+autAct.toFixed(2)+' €</span></div>':'')
    +'<div class="trow"><span class="trow-l">IEE (extraído)</span><span>'+(d.iee_act||0).toFixed(2)+' €</span></div>'
    +(servSum>0?'<div class="trow"><span class="trow-l">Servicios extra</span><span>'+servSum.toFixed(2)+' €</span></div>':'')
    +'<div class="trow"><span class="trow-l">IVA ('+d.iva_pct+'%)</span><span>'+ivaActCalc.toFixed(2)+' €</span></div>'
    +'<div class="trow" style="margin-bottom:0"><span class="trow-l" style="color:var(--tx);font-weight:600">TOTAL FACTURA</span>'
    +'<span style="font-size:19px;font-weight:800;font-family:\'Syne\',sans-serif">'+calcTotalAct.toFixed(2)+' €</span></div>';

  // Filter and rank offers
  const ofertasFiltradas=ST.ofertas.filter(function(o){return ofertaMatchesFact(o,d);});
  if(!ofertasFiltradas.length){
    $('rankDiv').innerHTML='<div class="empty"><div class="eico">⚡</div>'
      +(ST.ofertas.length===0?'No hay ofertas en la base de datos. Ve a "Ofertas DB" para añadir.'
        :'No hay ofertas compatibles con Tarifa '+d.tarifa+', Potencia '+d.potencia_kw+' kW'+(d.consumo_anual?' y Consumo '+d.consumo_anual+' kWh/año':'')+'.')
      +'</div>';
    return;
  }

  let res=ofertasFiltradas.map(function(o){
    const c=calcOfr(d,o);
    const ahorro=calcTotalAct-c.total;
    const ahorroPct=calcTotalAct>0?(ahorro/calcTotalAct*100):0;
    const ahorroAnual=d.dias>0?(ahorro/d.dias*365):0;
    return Object.assign({},o,c,{ahorro,ahorroPct,ahorroAnual});
  });
  res.sort(function(a,b){return b.comision-a.comision||b.ahorro-a.ahorro;});
  ST._res=res;

  const isAdmin=ST.user?.role==='admin';

  // Comercial: filter logic
  let display=res;
  if(!isAdmin){
    const con7=res.filter(function(r){return r.ahorroPct>=7;});
    if(con7.length>0){
      // Best commission among those with >7% savings
      display=[con7[0]];
    } else {
      const conAhorro=res.filter(function(r){return r.ahorro>0;});
      if(conAhorro.length>0){
        display=[conAhorro[0]]; // best commission with any savings
      } else {
        $('rankDiv').innerHTML='<div class="no-oferta"><div style="font-size:24px;margin-bottom:8px">ℹ️</div>'
          +'<div style="font-weight:700;font-size:13px;margin-bottom:6px">De momento no hay una oferta mejor</div>'
          +'<div style="font-size:11px;opacity:.8">Se evaluará en futuras ofertas. Consulta con Administración.</div></div>';
        return;
      }
    }
  }

  $('rankDiv').innerHTML=display.map(function(r,i){
    const badge = i === 0 && !isAdmin ? '<span class="bdg bdg-g">✨ La mejor opción</span>'
      : i === 0 ? '<span class="bdg bdg-g">✨ Recomendada</span>'
      : i === 1 ? '<span class="bdg bdg-b">Opción #2</span>' : '';
    
    const isSelected = ST.sel?.id === r.id;
    return '<div class="ofr-card anim-in ' + (i === 0 ? 'top' : '') + ' ' + (isSelected ? 'sel' : '') + '" onclick="selOfr(\'' + r.id + '\',' + i + ')" style="animation-delay:'+(i*0.05)+'s">'
      + '<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px">'
        + '<div><div class="ofr-name">' + r.nombre + '</div><div class="ofr-sub">' + r.comercializadora + ' · ' + r.tipo + '</div></div>'
        + badge
      + '</div>'
      + '<div class="ofr-metrics">'
        + '<div class="met"><div class="met-l">Total Estimado</div><div class="met-v">' + r.total.toFixed(2) + ' €</div></div>'
        + '<div class="met"><div class="met-l">Ahorro Mensual</div><div class="met-v ' + (r.ahorro >= 0 ? 'g' : 'r') + '">' + (r.ahorro >= 0 ? '+' : '') + r.ahorro.toFixed(2) + ' €</div></div>'
        + (isAdmin ? '<div class="met"><div class="met-l">Comisión</div><div class="met-v y">' + r.comision.toFixed(2) + ' €</div></div>' : '<div class="met"><div class="met-l">Ahorro %</div><div class="met-v g">' + r.ahorroPct.toFixed(1) + '%</div></div>')
      + '</div>'
      + '</div>';
  }).join('');
}

function selOfr(id){
  const r=ST._res.find(function(x){return x.id===id;});
  if(!r) return;
  ST.sel=r;
  document.querySelectorAll('.ofr-card').forEach(function(c){c.classList.remove('sel');});
  event.currentTarget.classList.add('sel');
  const d=getForm(), isAdmin=ST.user?.role==='admin';
  $('detDiv').innerHTML='<div class="card anim-in" style="margin-bottom:0">'
    +'<div class="ct">Detalles de la Oferta</div>'
    +'<div style="font-family:\'Outfit\',sans-serif;font-weight:700;font-size:18px;margin-bottom:4px">'+r.nombre+'</div>'
    +'<div style="color:var(--t2);font-size:12px;margin-bottom:20px;display:flex;align-items:center;gap:8px">'
      +'<span>'+r.comercializadora+'</span> <span style="opacity:0.3">|</span> <span>'+r.tipo+'</span> <span style="opacity:0.3">|</span> <span>'+(r.permanencia||t('Sin permanencia'))+'</span>'
    +'</div>'
    +'<div class="trow"><span class="trow-l">Término Potencia</span><span>'+r.tPot.toFixed(2)+' €</span></div>'
    +'<div class="trow"><span class="trow-l">Término Energía</span><span>'+r.tEn.toFixed(2)+' €</span></div>'
    +(r.compNva>0?'<div class="trow"><span class="trow-l">Compensación Autoconsumo</span><span style="color:var(--ok)">-'+r.compNva.toFixed(2)+' €</span></div>':'')
    +'<div class="trow"><span class="trow-l">Impuesto Eléctrico (IEE)</span><span>'+r.iee.toFixed(2)+' €</span></div>'
    +'<div class="trow"><span class="trow-l">IVA ('+d.iva_pct+'%)</span><span>'+r.iva.toFixed(2)+' €</span></div>'
    +'<div class="trow" style="margin-top:12px;background:rgba(255,255,255,0.05);border-color:var(--b2)"><span class="trow-l" style="color:var(--tx);font-weight:700">TOTAL ESTIMADO</span><span style="font-size:20px;font-weight:800;font-family:\'Outfit\',sans-serif;color:var(--acc)">'+r.total.toFixed(2)+' €</span></div>'
    +'<div class="ahorro-box">'
      +'<div>'
        +'<div style="font-weight:700;font-size:12px;color:var(--ok);letter-spacing:1px">AHORRO ESTIMADO</div>'
        +'<div style="font-size:11px;color:var(--ok);opacity:0.8;margin-top:2px">Anual: ~'+r.ahorroAnual.toFixed(0)+' €/año</div>'
      +'</div>'
      +'<div class="ahorro-v">'+(r.ahorro>=0?'+':'')+r.ahorro.toFixed(2)+' €</div>'
    +'</div>'
    +(isAdmin?'<div class="com-box"><div style="font-size:10px;color:var(--t3);margin-bottom:6px;font-weight:700;text-transform:uppercase;letter-spacing:1px">Beneficio Comercial</div>'
      +'<div class="com-v">'+r.comision.toFixed(2)+' €</div>'
      +'<div style="font-size:11px;color:var(--t2);margin-top:4px;line-height:1.4">'+(r.tipo_comision==='consumo'?'Calculado como '+r.coef_reparto+'% de comisión sobre '+(d.consumo_anual||0)+' kWh':'Comisión fija prorrateada')+'</div></div>':'')
    +'</div>';
}

// ════════════════════════════════════════════
// PDF
// ════════════════════════════════════════════
function genPDF(){
  if(!ST.sel){alert('Selecciona una oferta primero');return;}
  const d=getForm(), r=ST.sel;
  const asesor=($('g_asesor')?.value||'').trim();
  const fechaProp=$('g_fecha')?.value||new Date().toISOString().split('T')[0];
  const validezDias=r.validez||7;
  const fechaFmt=function(iso){if(!iso)return'';const p=iso.split('-');return p[2]+'/'+p[1]+'/'+p[0];};
  const fmt=function(v){return v===0?'— €':v.toFixed(2)+' €';};
  const fmtP=function(v){return v===0?'—':v.toFixed(5);};
  const servSum=d.servicio||0;
  const baseIVAAct=(d.total_factura-d.iva_act)+servSum;
  const ivaActCalc=d.iva_act+(servSum*(d.iva_pct/100));
  const calcTotalAct=baseIVAAct+ivaActCalc;
  
  const ahorroEur=calcTotalAct-r.total;
  const ahorroPct=calcTotalAct>0?(ahorroEur/calcTotalAct*100):0;
  const ahorroAnual=d.dias>0?(ahorroEur/d.dias*365):0;
  const tPotAct=d.pot_p.reduce((s,l)=>s+l.importe,0);
  const dtoActPct=d.dto_en_act_pct||0;
  const ieeAct=d.iee_act||0, ivaAct=ivaActCalc;
  const dtoEnNvaPct=r.dto_energia_por_periodo?0:(r.dto_energia_global||0);
  let tEnNvaBase=0, tEnActBase=0;
  let rowsPot='', rowsEn='';
  
  PS.forEach(p=>{
    const pLines = d.pot_p.filter(x=>x.per===p);
    const kwNva = pLines.length>0 ? Math.max(...pLines.map(x=>x.kw)) : 0;
    let ppNva = r['pp_'+p.toLowerCase()]||0;
    if(d.tarifa.startsWith('2.0') && p==='P3' && !ppNva) ppNva=r.pp_p2||0;
    const impNva = kwNva * ppNva * d.dias;
    if(pLines.length===0){
       rowsPot+='<tr><td class="per">'+p+'</td><td class="num">—</td><td class="num">—</td><td class="num bold">— €</td><td class="sep"></td><td class="num">—</td><td class="num">'+fmtP(ppNva)+'</td><td class="num bold nva">— €</td></tr>';
    } else {
       pLines.forEach((l,i)=>{
         const precioAct = (l.kw>0 && d.dias>0) ? l.importe/(l.kw*d.dias) : 0;
         const isLast = (i===pLines.length-1);
         // For multiple lines, we only show the New Offer total on the last line for cleaner UI, or just show it on the first
         rowsPot+='<tr><td class="per">'+(i===0?p:'')+'</td><td class="num">'+(l.kw>0?l.kw.toLocaleString('es-ES',{minimumFractionDigits:3}):'—')+'</td><td class="num">'+fmtP(precioAct)+'</td><td class="num bold">'+(l.importe>0?fmt(l.importe):'— €')+'</td><td class="sep"></td><td class="num">'+(i===0&&kwNva>0?kwNva.toLocaleString('es-ES',{minimumFractionDigits:3}):'')+'</td><td class="num">'+(i===0?fmtP(ppNva):'')+'</td><td class="num bold nva">'+(i===0&&(impNva>0)?fmt(impNva):'')+'</td></tr>';
       });
    }
  });

  // Para la columna derecha (Nueva Oferta) usamos lecturas reales si existen
  const simByPer = d.lec_by_per || {};

  PS.forEach((p,idx)=>{
    const eLines = d.en_p.filter(x=>x.per===p);
    const dtoP=r.dto_energia_por_periodo?(r['dto_e_p'+(idx+1)]||0)/100:dtoEnNvaPct/100;
    const epNva=r['ep_'+p.toLowerCase()]||0;
    const kwhSim = simByPer[p]||0;  // kWh reales para simulación
    const impNvaSim = kwhSim*epNva*(1-dtoP);
    tEnNvaBase += kwhSim*epNva;
    
    if(eLines.length===0 && kwhSim===0){
       rowsEn+='<tr><td class="per">'+p+'</td><td class="num">—</td><td class="num">—</td><td class="num bold">— €</td><td class="sep"></td><td class="num">—</td><td class="num">'+fmtP(epNva)+'</td><td class="num bold nva">— €</td></tr>';
    } else if(eLines.length===0 && kwhSim>0){
       // No hay línea de facturación pero sí hay lectura real → mostrar solo la derecha
       rowsEn+='<tr><td class="per">'+p+'</td><td class="num">—</td><td class="num">—</td><td class="num bold">— €</td><td class="sep"></td><td class="num">'+kwhSim.toLocaleString('es-ES',{minimumFractionDigits:3})+'</td><td class="num">'+fmtP(epNva)+'</td><td class="num bold nva">'+(impNvaSim>0?fmt(impNvaSim):'— €')+'</td></tr>';
    } else {
       // Hay líneas de facturación → mostrarlas todas en la izquierda, y en la derecha solo la primera fila con el total simulado
       eLines.forEach((l,i)=>{
         const impAB=l.kwh*l.precio; tEnActBase+=impAB;
         const esUltimaFila=(i===eLines.length-1);
         rowsEn+='<tr>';
         rowsEn+='<td class="per">'+(i===0?p:'')+'</td>';
         rowsEn+='<td class="num">'+(l.kwh>0?l.kwh.toLocaleString('es-ES',{minimumFractionDigits:3}):'—')+'</td>';
         rowsEn+='<td class="num">'+(l.precio>0?fmtP(l.precio):'—')+'</td>';
         rowsEn+='<td class="num bold">'+(impAB>0?fmt(impAB):'— €')+'</td>';
         rowsEn+='<td class="sep"></td>';
         if(i===0){
           // Primera fila: columna derecha muestra kWh reales (lecturas) y precio nueva oferta
           rowsEn+='<td class="num">'+(kwhSim>0?kwhSim.toLocaleString('es-ES',{minimumFractionDigits:3}):'—')+'</td>';
           rowsEn+='<td class="num">'+(epNva>0?fmtP(epNva):'—')+'</td>';
           rowsEn+='<td class="num bold nva">'+(impNvaSim>0?fmt(impNvaSim):'— €')+'</td>';
         } else {
           // Resto de filas: celda derecha vacía (el total ya está en la primera fila)
           rowsEn+='<td class="num" style="background:#f0fafb"></td><td class="num" style="background:#f0fafb"></td><td class="num bold nva"></td>';
         }
         rowsEn+='</tr>';
       });
    }
  });

  const dtoActEur=tEnActBase*(dtoActPct/100), tEnActNeto=tEnActBase-dtoActEur;
  const dtoNvaEur=tEnNvaBase*(dtoEnNvaPct/100);
  let rowsExtras='';
  if((d.iee_extras||[]).length>0){
    rowsExtras+='<tr><td colspan="8" class="sec-hdr">OTROS CONCEPTOS</td></tr>';
    d.iee_extras.forEach(function(e){rowsExtras+='<tr><td colspan="3" style="padding:4px 8px;border-bottom:1px solid #e5e7eb">'+e.nombre+'</td><td class="num bold">'+fmt(e.importe)+'</td><td class="sep"></td><td colspan="2"></td><td class="num bold nva">'+(e.mantiene?fmt(e.importe):'— €')+'</td></tr>';});
  }
  const autActEur=d.tiene_autoconsumo?(d.autoconsumo_kwh||0)*(d.autoconsumo_precio_kwh||0):0;
  const autNvaEur=r.compNva||0;
  const logoSVG='<svg width="110" height="52" viewBox="0 0 110 52" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="13" r="12" fill="#3d4044"/><text x="14" y="18" text-anchor="middle" fill="white" font-size="10" font-family="Arial" font-weight="bold">G</text><circle cx="14" cy="39" r="12" fill="#2cb5ad"/><text x="14" y="44" text-anchor="middle" fill="white" font-size="10" font-family="Arial" font-weight="bold">G</text><text x="32" y="18" font-family="Arial" font-size="12" font-weight="900" fill="#3d4044">GESTION</text><text x="32" y="33" font-family="Arial" font-size="12" font-weight="900" fill="#3d4044">GROUP</text><text x="32" y="48" font-family="Arial" font-size="6.5" fill="#2cb5ad" letter-spacing="2">SOLUCIONES ENERGÉTICAS</text></svg>';
  const w=window.open('','_blank');
  w.document.write('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><style>'
+'*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,sans-serif;font-size:10.5px;color:#2d3138;padding:16px 20px}'
+'.hdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;padding-bottom:9px;border-bottom:3px solid #2cb5ad}'
+'.hdr-right{text-align:right;font-size:9.5px;color:#6b7280;line-height:1.6}.hdr-right b{font-size:11px;color:#2d3138}'
+'.offer-bar{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;background:#f0fafb;border:1px solid #b2e0de;border-radius:6px;padding:7px 10px;margin-bottom:9px;font-size:9.5px}'
+'.offer-bar .lbl{color:#6b7280;margin-bottom:1px}.offer-bar .val{font-weight:800;font-size:10.5px}.offer-bar .val.teal{color:#2cb5ad}'
+'table{width:100%;border-collapse:collapse;font-size:9.5px}'
+'.th-act{background:#3d4044;color:#fff;padding:4px 7px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;text-align:center}'
+'.th-nva{background:#2cb5ad;color:#fff;padding:4px 7px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;text-align:center}'
+'.sec-hdr{background:#f3f4f6;color:#3d4044;padding:4px 7px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #e5e7eb}'
+'.col-hdr{background:#f9fafb;color:#374151;padding:3px 7px;font-size:8.5px;font-weight:600;text-align:center;border-bottom:1px solid #e5e7eb}'
+'.per{padding:3px 7px;border-bottom:1px solid #f3f4f6;color:#2cb5ad;font-weight:700;width:26px;text-align:center}'
+'.num{padding:3px 7px;border-bottom:1px solid #f3f4f6;text-align:right}.num.bold{font-weight:700}.num.nva{background:#f0fafb}'
+'.sep{width:5px;background:#e5e7eb;padding:0}'
+'.dto-row td{padding:2px 7px;border-bottom:1px solid #e5e7eb;font-size:8.5px;color:#6b7280;font-style:italic}'
+'.dto-row .red{color:#dc2626;font-style:normal}'
+'.tot-row td{background:#f9fafb;font-weight:700;font-size:10.5px;padding:4px 7px;border-top:2px solid #d1d5db;border-bottom:1px solid #e5e7eb}'
+'.tot-row .nva{background:#e6f7f6;color:#1a7a75}'
+'.ext-row td{padding:3px 7px;border-bottom:1px solid #f3f4f6}.ext-row .nva{background:#f0fafb}'
+'.ahorro{background:linear-gradient(135deg,#e6f7f6,#d1f0ee);border:2px solid #2cb5ad;border-radius:7px;padding:11px 16px;display:flex;justify-content:space-between;align-items:center;margin:10px 0}'
+'.ahorro-lbl{font-weight:800;color:#1a7a75;font-size:11px}.ahorro-sub{font-size:9.5px;color:#2cb5ad;margin-top:2px}'
+'.ahorro-val .eur{font-size:22px;font-weight:900;color:#1a7a75;text-align:right}'
+'.ahorro-val .pct{font-size:13px;font-weight:700;color:#2cb5ad;text-align:right}'
+'.it{width:100%;border-collapse:collapse;margin-bottom:9px}'
+'.it th{background:#f3f4f6;padding:4px 9px;font-size:8.5px;font-weight:700;text-align:left;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #e5e7eb}'
+'.it td{padding:4px 9px;border-bottom:1px solid #f3f4f6;font-size:10px}'
+'.footer-bar{display:flex;justify-content:space-between;align-items:flex-end;margin-top:10px;padding-top:8px;border-top:2px solid #2cb5ad}'
+'.asesor-box{background:#f0fafb;border:1px solid #b2e0de;border-radius:6px;padding:7px 14px}'
+'.asesor-lbl{font-size:8px;color:#6b7280;letter-spacing:.5px;text-transform:uppercase;margin-bottom:2px}'
+'.asesor-name{font-size:12px;font-weight:800;color:#2d3138}'
+'.foot-legal{font-size:8px;color:#9ca3af;max-width:400px;line-height:1.5;text-align:right}'
+'@media print{body{padding:8px 12px}@page{margin:7mm}}'
+'</style></head><body>'
+'<div class="hdr"><div><div style="margin-bottom:5px">'+logoSVG+'</div><div style="font-size:16px;font-weight:900;color:#2d3138;letter-spacing:-.3px">'+t('ESTUDIO COMPARATIVO ENERGÉTICO')+'</div><div style="font-size:9px;color:#6b7280;margin-top:2px">'+t('Preparado el')+' '+fechaFmt(fechaProp)+' · ' + t('Válido') + ' '+validezDias+' '+t('días')+'</div></div>'
+'<div class="hdr-right"><b>'+( d.cliente||'' )+'</b><br>'+(d.cups||'')+'<br>'+(d.direccion?d.direccion+(d.cp?', '+d.cp:''):'')+'<br>'+t('Tarifa')+' '+d.tarifa+' · '+d.potencia_kw+' '+t('kW')+' · '+d.dias+' '+t('días')+'</div></div>'
+'<div class="offer-bar"><div><div class="lbl">'+t('COMERCIALIZADORA ACTUAL')+'</div><div class="val">'+(d.comercializadora||'—')+'</div></div><div><div class="lbl">'+t('OFERTA')+'</div><div class="val teal">'+r.nombre+'</div></div><div><div class="lbl">'+t('PERMANENCIA')+'</div><div class="val">'+(r.permanencia||t('Sin permanencia'))+'</div></div><div><div class="lbl">'+t('TIPO')+'</div><div class="val">'+t(r.tipo)+'</div></div></div>'
+'<table><thead><tr><td colspan="4" class="th-act" style="text-align:center">'+t('FACTURACIÓN ACTUAL')+' · '+(d.comercializadora||'')+'</td><td class="sep"></td><td colspan="3" class="th-nva" style="text-align:center">'+t('NUEVA FACTURACIÓN')+' · '+r.nombre+' · '+r.comercializadora+'</td></tr>'
+'<tr><td colspan="8" class="sec-hdr">'+t('T. FIJO — POTENCIA')+'</td></tr>'
+'<tr><th class="col-hdr" style="width:26px">'+t('PER.')+'</th><th class="col-hdr">'+t('kW')+'</th><th class="col-hdr">'+t('€/kW·día')+'</th><th class="col-hdr">'+t('TOTALES')+'</th><td class="sep"></td><th class="col-hdr">'+t('kW')+'</th><th class="col-hdr">'+t('€/kW·día')+'</th><th class="col-hdr" style="background:#e6f7f6">'+t('TOTALES')+'</th></tr></thead>'
+'<tbody>'+rowsPot
+'<tr class="dto-row"><td colspan="3">'+t('DTO.')+' '+((r.dto_potencia||0)>0?(r.dto_potencia).toFixed(0)+'%':'0%')+'</td><td class="num">— €</td><td class="sep"></td><td colspan="2">'+t('DTO.')+' '+((r.dto_potencia||0)>0?(r.dto_potencia).toFixed(0)+'%':'0%')+'</td><td class="num nva">'+((r.dto_potencia||0)>0?'- '+fmt(tPotAct*(r.dto_potencia/100)):'— €')+'</td></tr>'
+'<tr class="tot-row"><td colspan="3">'+t('TOTAL POTENCIA')+'</td><td class="num">'+fmt(tPotAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.tPot)+'</td></tr>'
+'<tr><td colspan="8" class="sec-hdr">'+t('T. VARIABLE — ENERGÍA')+'</td></tr>'
+'<tr><th class="col-hdr">'+t('PER.')+'</th><th class="col-hdr">'+t('kWh')+'</th><th class="col-hdr">'+t('€/kWh')+'</th><th class="col-hdr">'+t('TOTALES')+'</th><td class="sep"></td><th class="col-hdr">'+t('kWh')+'</th><th class="col-hdr">'+t('€/kWh')+'</th><th class="col-hdr" style="background:#e6f7f6">'+t('TOTALES')+'</th></tr>'
+rowsEn
+'<tr class="dto-row"><td colspan="3">'+t('DTO.')+' '+(dtoActPct>0?dtoActPct.toFixed(0)+'%':'')+'</td><td class="num red">'+(dtoActEur>0?'- '+fmt(dtoActEur):'— €')+'</td><td class="sep"></td><td colspan="2">'+t('DTO.')+' '+(dtoEnNvaPct>0?dtoEnNvaPct.toFixed(0)+'%':'')+'</td><td class="num nva red">'+(dtoNvaEur>0?'- '+fmt(dtoNvaEur):'— €')+'</td></tr>'
+'<tr class="tot-row"><td colspan="3">'+t('TOTAL ENERGÍA')+'</td><td class="num">'+fmt(tEnActNeto)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.tEn)+'</td></tr>'
+rowsExtras
+'<tr><td colspan="8" class="sec-hdr">'+t('IMPUESTOS Y OTROS')+'</td></tr>'
+(d.tiene_autoconsumo?'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('Compensación Autoconsumo')+' ('+d.autoconsumo_kwh+' '+t('kWh')+')</td><td class="num bold" style="color:#16a34a">-'+fmt(autActEur)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva" style="color:#16a34a">-'+fmt(autNvaEur)+'</td></tr>':'')
+(d.reactiva>0?'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('Energía Reactiva')+'</td><td class="num bold">'+fmt(d.reactiva)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">— €</td></tr>':'')
+(d.alquiler_equipos>0?'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('Alquiler Equipos')+'</td><td class="num bold">'+fmt(d.alquiler_equipos)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(d.alquiler_equipos)+'</td></tr>':'')
+'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('Imp. Electricidad (IEE)')+' '+d.iee_pct+'%</td><td class="num bold">'+fmt(ieeAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.iee)+'</td></tr>'
+(d.bono_social>0?'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('Financiación Bono Social')+'</td><td class="num bold">'+fmt(d.bono_social)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(d.bono_social)+'</td></tr>':'')
+(d.servicio>0?'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('Servicios')+'</td><td class="num bold">'+fmt(d.servicio)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">— €</td></tr>':'')
+'<tr class="ext-row" style="border-top:1px solid #d1d5db"><td colspan="3" style="padding:3px 7px;color:#9ca3af;font-size:8.5px">'+t('Base Imponible')+'</td><td class="num" style="color:#9ca3af;font-size:8.5px">'+fmt(baseIVAAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva" style="color:#9ca3af;font-size:8.5px">'+fmt(r.baseIVA)+'</td></tr>'
+'<tr class="ext-row"><td colspan="3" style="padding:3px 7px">'+t('IVA')+' ('+d.iva_pct+'%)</td><td class="num bold">'+fmt(ivaAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.iva)+'</td></tr>'
+'<tr class="tot-row"><td colspan="3" style="font-size:12px">'+t('TOTAL')+'</td><td class="num" style="font-size:13px">'+fmt(calcTotalAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva" style="font-size:13px;color:#1a7a75">'+fmt(r.total)+'</td></tr>'
+'</tbody></table>'
+'<div class="ahorro"><div><div class="ahorro-lbl">'+t('AHORRO ESTIMADO EN FACTURA')+'</div><div class="ahorro-sub">'+t('Ahorro anual estimado')+': '+ahorroAnual.toFixed(0)+' '+t('€/año')+'</div></div>'
+'<div class="ahorro-val"><div class="eur">'+(ahorroEur>=0?'+':'')+fmt(ahorroEur)+'</div><div class="pct">'+(ahorroEur>=0?'+':'')+ahorroPct.toFixed(2)+' %</div></div></div>'
+'<table class="it"><thead><tr><th>'+t('COMERCIALIZADORA')+'</th><th>'+t('TARIFA')+'</th><th>'+t('TIPO PRECIO')+'</th><th>'+t('PERMANENCIA')+'</th><th>'+t('VALIDEZ')+'</th></tr></thead>'
+'<tbody><tr><td>'+r.comercializadora+'</td><td>'+r.tarifa+'</td><td>'+t(r.tipo)+'</td><td>'+(r.permanencia||t('Sin permanencia'))+'</td><td>'+validezDias+' '+t('días')+'</td></tr></tbody></table>'
+'<div class="footer-bar"><div class="asesor-box"><div class="asesor-lbl">'+t('Nombre del Asesor')+'</div><div class="asesor-name">'+(asesor||'_________________________')+'</div></div>'
+'<div class="foot-legal">'+t('Los precios de potencia y energía incluyen todos los PEAJES/ATR.')+'<br>'+t('Cálculos de carácter informativo no vinculantes.')+'<br>'+t('Fecha propuesta')+': '+fechaFmt(fechaProp)+'</div></div>'
+'</body></html>');
  w.document.close(); setTimeout(function(){w.print();},700);
}

// ════════════════════════════════════════════
// OFERTAS DB
// ════════════════════════════════════════════
function togDpp(){const c=$('o_dpp').checked; $('dppDet').style.display=c?'block':'none';}
function togComision(){
  const v=$('o_tco').value;
  $('f_comfijo').style.display=v==='fijo'?'':'none';
  $('f_comconsumo').style.display=v==='consumo'?'':'none';
}

function openMod(id){
  ST.editOfrId=id;
  const flds=['nom','com','tar','tip','per','val','pmin','pmax','cmin','cmax','tco','co','coef','fee','comp','dp','de','pp1','pp2','pp3','pp4','pp5','pp6','ep1','ep2','ep3','ep4','ep5','ep6','de1','de2','de3','de4','de5','de6'];
  if(id){
    const o=ST.ofertas.find(function(x){return x.id===id;});
    $('modOfrT').textContent='Editar Oferta';
    const map={nom:'nombre',com:'comercializadora',tar:'tarifa',tip:'tipo',per:'permanencia',val:'validez',pmin:'pot_min',pmax:'pot_max',cmin:'consumo_min',cmax:'consumo_max',tco:'tipo_comision',co:'comision',coef:'coef_reparto',fee:'fee_mwh',comp:'compensacion',dp:'dto_potencia',de:'dto_energia_global',pp1:'pp_p1',pp2:'pp_p2',pp3:'pp_p3',pp4:'pp_p4',pp5:'pp_p5',pp6:'pp_p6',ep1:'ep_p1',ep2:'ep_p2',ep3:'ep_p3',ep4:'ep_p4',ep5:'ep_p5',ep6:'ep_p6',de1:'dto_e_p1',de2:'dto_e_p2',de3:'dto_e_p3',de4:'dto_e_p4',de5:'dto_e_p5',de6:'dto_e_p6'};
    flds.forEach(function(f){const el=$('o_'+f);if(el&&o[map[f]]!==undefined)el.value=o[map[f]];});
    $('o_dpp').checked=!!o.dto_energia_por_periodo;
  } else {
    $('modOfrT').textContent='Nueva Oferta';
    flds.forEach(function(f){const el=$('o_'+f);if(el)el.value='';});
    $('o_val').value=7;$('o_pmin').value=0;$('o_pmax').value=9999;$('o_cmin').value=0;$('o_cmax').value=99999999;
    $('o_dp').value=0;$('o_de').value=0;$('o_comp').value=0;$('o_tco').value='fijo';$('o_dpp').checked=false;
  }
  togDpp();togComision();
  $('modalOfr').style.display='flex'; document.body.style.overflow='hidden';
}
function closeMod(id){$(id).style.display='none'; document.body.style.overflow='';}

function saveOfr(){
  const nom=$('o_nom').value.trim(); if(!nom){alert('El nombre es obligatorio');return;}
  const o={
    id:ST.editOfrId||Date.now().toString(), nombre:nom,
    comercializadora:$('o_com').value, tarifa:$('o_tar').value, tipo:$('o_tip').value,
    permanencia:$('o_per').value, validez:parseInt($('o_val').value)||7,
    pot_min:n($('o_pmin').value), pot_max:n($('o_pmax').value)||9999,
    consumo_min:n($('o_cmin').value), consumo_max:n($('o_cmax').value)||99999999,
    tipo_comision:$('o_tco').value, comision:n($('o_co').value),
    coef_reparto:n($('o_coef').value), fee_mwh:n($('o_fee').value),
    compensacion:n($('o_comp').value), dto_potencia:n($('o_dp').value),
    dto_energia_global:n($('o_de').value), dto_energia_por_periodo:$('o_dpp').checked,
    pp_p1:n($('o_pp1').value),pp_p2:n($('o_pp2').value),pp_p3:n($('o_pp3').value),
    pp_p4:n($('o_pp4').value),pp_p5:n($('o_pp5').value),pp_p6:n($('o_pp6').value),
    ep_p1:n($('o_ep1').value),ep_p2:n($('o_ep2').value),ep_p3:n($('o_ep3').value),
    ep_p4:n($('o_ep4').value),ep_p5:n($('o_ep5').value),ep_p6:n($('o_ep6').value),
    dto_e_p1:n($('o_de1').value),dto_e_p2:n($('o_de2').value),dto_e_p3:n($('o_de3').value),
    dto_e_p4:n($('o_de4').value),dto_e_p5:n($('o_de5').value),dto_e_p6:n($('o_de6').value),
  };
  if(ST.editOfrId){const i=ST.ofertas.findIndex(function(x){return x.id===ST.editOfrId;});ST.ofertas[i]=o;}
  else ST.ofertas.push(o);
  saveOfertasToServer(); updCnt(); closeMod('modalOfr'); renderOfrList();
  applyLang();
}
function delOfr(id){
  if(!confirm('¿Eliminar esta oferta?'))return;
  ST.ofertas=ST.ofertas.filter(function(x){return x.id!==id;});
  saveOfertasToServer(); updCnt(); renderOfrList();
  applyLang();
}
function renderOfrList(){
  const el=$('ofrList');
  if(!ST.ofertas.length){el.innerHTML='<div class="empty"><div class="eico">⚡</div>No hay ofertas. Añade tu primera oferta.</div>';return;}
  el.innerHTML=ST.ofertas.map(function(o, i){
    return '<div class="card anim-in" style="margin-bottom:12px; animation-delay:'+(i*0.03)+'s">'
      +'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">'
        +'<div><div style="font-family:\'Outfit\',sans-serif;font-weight:700;font-size:15px;color:var(--tx)">'+o.nombre+' <span class="tag t">'+o.tarifa+'</span> <span class="tag">'+o.tipo+'</span></div>'
        +'<div style="font-size:12px;color:var(--t2);margin-top:4px">'+o.comercializadora+' · '+(o.permanencia||'Sin permanencia')+'</div></div>'
        +'<div style="display:flex;gap:8px;flex-shrink:0"><button class="btn btn-s btn-sm" onclick="openMod(\''+o.id+'\')">✎</button><button class="btn btn-d btn-sm" onclick="delOfr(\''+o.id+'\')">✕</button></div>'
      +'</div>'
      +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'
        +'<div><div style="font-size:10px;color:var(--t3);margin-bottom:6px;font-weight:700;text-transform:uppercase">Potencia (€/kW/día)</div><div style="display:flex;gap:4px;flex-wrap:wrap">'+PS.map(function(p){return '<span style="background:rgba(0,0,0,0.2);border:1px solid var(--b1);border-radius:6px;padding:3px 8px;font-size:12px;font-family:\'DM Mono\',monospace"><span style="color:var(--acc);font-weight:700">'+p+'</span> '+(o['pp_'+p.toLowerCase()]||0)+'</span>';}).join('')+'</div></div>'
        +'<div><div style="font-size:10px;color:var(--t3);margin-bottom:6px;font-weight:700;text-transform:uppercase">Energía (€/kWh)</div><div style="display:flex;gap:4px;flex-wrap:wrap">'+PS.map(function(p){return '<span style="background:rgba(0,0,0,0.2);border:1px solid var(--b1);border-radius:6px;padding:3px 8px;font-size:12px;font-family:\'DM Mono\',monospace"><span style="color:var(--acc2);font-weight:700">'+p+'</span> '+(o['ep_'+p.toLowerCase()]||0)+'</span>';}).join('')+'</div></div>'
      +'</div></div>';
  }).join('');
}

// ════════════════════════════════════════════
// USUARIOS
// ════════════════════════════════════════════
function renderUsersTable(){
  const isAdmin=ST.user?.role==='admin';
  $('cfg-users-title').textContent=isAdmin?'👤 Gestión de Usuarios':'👤 Mi Usuario';
  const users=isAdmin?ST.usuarios:ST.usuarios.filter(function(u){return u.id===ST.user?.id;});
  if(!users.length){$('cfg-users-content').innerHTML='<div style="color:var(--t2);font-size:12px">No hay usuarios.</div>';return;}
  $('cfg-users-content').innerHTML='<table class="users-table"><thead><tr><th>Nombre</th><th>Email</th><th>Perfil</th><th></th></tr></thead><tbody>'
    +users.map(function(u){
      const canEdit=isAdmin||(u.id===ST.user?.id);
      const canDel=isAdmin&&u.id!==ST.user?.id;
      return '<tr><td>'+u.nombre+'</td><td>'+u.email+'</td>'
        +'<td><span class="tag '+(u.role==='admin'?'g t':'')+'">'+( u.role==='admin'?'Admin':'Comercial' )+'</span></td>'
        +'<td style="display:flex;gap:5px">'
          +(canEdit?'<button class="btn btn-s btn-sm" onclick="openUserMod(\''+u.id+'\')">✎ Editar</button>':'')
          +(canDel?'<button class="btn btn-d" onclick="delUser(\''+u.id+'\')">🗑️</button>':'')
        +'</td></tr>';
    }).join('')+'</tbody></table>';
}

function openUserMod(id){
  ST.editUserId=id;
  $('modUserT').textContent=id?'Editar Usuario':'Nuevo Usuario';
  const isAdmin=ST.user?.role==='admin';
  $('u_role_field').style.display=isAdmin?'':'none';
  if(id){
    const u=ST.usuarios.find(function(x){return x.id===id;});
    $('u_nombre').value=u.nombre||''; $('u_email').value=u.email||'';
    $('u_pass').value=''; $('u_role').value=u.role||'comercial';
  } else {
    $('u_nombre').value=''; $('u_email').value=''; $('u_pass').value=''; $('u_role').value='comercial';
  }
  $('modalUser').style.display='flex'; document.body.style.overflow='hidden';
}
async function saveUser(){
  const nombre=$('u_nombre').value.trim(), email=$('u_email').value.trim();
  const pass=$('u_pass').value, role=$('u_role').value;
  if(!nombre||!email){alert('Nombre y email son obligatorios');return;}
  try{
    const r=await fetch('/api/usuarios',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({action:ST.editUserId?'update':'create', id:ST.editUserId||null, nombre, email, password:pass, role})
    });
    const d=await r.json();
    if(d.error){alert(d.error);return;}
    await loadUsuarios(); renderUsersTable(); closeMod('modalUser');
    // If user edited their own name, update topbar
    if(ST.editUserId===ST.user?.id){ST.user.nombre=nombre;$('ui_nombre').textContent=nombre;}
  }catch(e){alert('Error: '+e.message);}
}
async function delUser(id){
  if(!confirm('¿Eliminar usuario?'))return;
  await fetch('/api/usuarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'delete',id})});
  await loadUsuarios(); renderUsersTable();
  applyLang();
}
</script>
</body></html>"""

# ── SERVER ───────────────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def do_GET(self):
        if self.path in ('/', '/index.html'): self._html()
        elif self.path == '/api/ofertas':  self._respond(200, load_json(DB_OFERTAS, []))
        elif self.path == '/api/config':
            cfg = load_json(DB_CONFIG, {})
            safe = {k:v for k,v in cfg.items() if k != 'api_key'}
            safe['has_api_key'] = bool(cfg.get('api_key',''))
            self._respond(200, safe)
        elif self.path == '/api/comisiones':
            self._respond(200, load_json(DB_COMISIONES, []))
        elif self.path == '/api/usuarios': self._respond(200, self._safe_users())
        else: self.send_response(404); self.end_headers()

    def do_POST(self):
        body = self._read()
        if self.path == '/api/login':    self._login(body)
        elif self.path == '/api/claude': self._claude(body)
        elif self.path == '/api/ofertas':
            save_json(DB_OFERTAS, body); self._respond(200, {'ok': True})
        elif self.path == '/api/config':
            old = load_json(DB_CONFIG, {})
            if not body.get('api_key'): body['api_key'] = old.get('api_key','')
            save_json(DB_CONFIG, body); self._respond(200, {'ok': True})
        elif self.path == '/api/comisiones':
            save_json(DB_COMISIONES, body); self._respond(200, {'ok': True})
        elif self.path == '/api/usuarios': self._usuarios(body)
        else: self.send_response(404); self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def _read(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length))

    def _safe_users(self):
        users = load_json(DB_USUARIOS, [])
        return [{'id':u['id'],'nombre':u['nombre'],'email':u['email'],'role':u['role']} for u in users]

    def _html(self):
        body = HTML.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self._cors(); self.end_headers(); self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')

    def _login(self, body):
        email = body.get('email','').strip().lower()
        pw    = hash_pw(body.get('password',''))
        users = load_json(DB_USUARIOS, [])
        user  = next((u for u in users if u['email'].lower()==email and u['password']==pw), None)
        if user:
            self._respond(200, {'ok':True,'user':{'id':user['id'],'nombre':user['nombre'],'email':user['email'],'role':user['role']}})
        else:
            self._respond(200, {'ok':False,'error':'Credenciales incorrectas'})

    def _usuarios(self, body):
        action = body.get('action')
        users  = load_json(DB_USUARIOS, [])
        if action == 'create':
            if any(u['email'].lower()==body['email'].lower() for u in users):
                self._respond(200, {'error':'El email ya existe'}); return
            pw = hash_pw(body['password']) if body.get('password') else hash_pw('cambiar123')
            users.append({'id':str(int(time.time()*1000)),'nombre':body['nombre'],'email':body['email'],'password':pw,'role':body.get('role','comercial')})
        elif action == 'update':
            idx = next((i for i,u in enumerate(users) if u['id']==body['id']), None)
            if idx is not None:
                users[idx]['nombre'] = body['nombre']
                users[idx]['email']  = body['email']
                users[idx]['role']   = body.get('role', users[idx]['role'])
                if body.get('password'): users[idx]['password'] = hash_pw(body['password'])
        elif action == 'delete':
            users = [u for u in users if u['id'] != body['id']]
        save_json(DB_USUARIOS, users)
        self._respond(200, {'ok':True})

    def _claude(self, body):
        api_key  = load_json(DB_CONFIG, {}).get('api_key','')
        messages = body.get('messages',[])
        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=json.dumps({'model':'claude-opus-4-5','max_tokens':2000,'messages':messages}).encode(),
            headers={'Content-Type':'application/json','x-api-key':api_key,'anthropic-version':'2023-06-01'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read())
            self._respond(200, {'text': data['content'][0]['text']})
        except urllib.error.HTTPError as e:
            err = json.loads(e.read())
            self._respond(e.code, {'error': err.get('error',{}).get('message', str(err))})
        except Exception as e:
            self._respond(500, {'error': str(e)})

    def _respond(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self._cors(); self.end_headers(); self.wfile.write(body)

# ── MAIN ──────────────────────────────────────────────────────────────────────
def open_browser():
    time.sleep(1.2)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    print('='*48)
    print('  ⚡  ESTUDIO LUZ v2.0')
    print('='*48)
    print(f'  Abriendo Chrome en http://localhost:{PORT}')
    print()
    print('  USUARIOS POR DEFECTO:')
    print('  Admin:     admin@gestiongroup.es / admin123')
    print('  Comercial: comercial@gestiongroup.es / comercial123')
    print()
    print('  Ctrl+C para detener.')
    print('='*48)
    threading.Thread(target=open_browser, daemon=True).start()
    server = http.server.HTTPServer(('localhost', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Servidor detenido.')
