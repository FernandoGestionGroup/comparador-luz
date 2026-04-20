
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
    "Autoconsumo": "Autoconsum", "Esta factura tiene autoconsumo": "This invoice has self-consumption", "kWh GENERADOS / COMPENSADOS": "GENERATED / COMPENSATED kWh",
    "€/kWh PRECIO COMPENSACIÓN ACTUAL": "CURRENT €/kWh COMPENSATION PRICE", "TOTAL COMPENSACIÓN (€)": "TOTAL COMPENSATION (€)", "La compensación se calculará automáticamente: kWh × €/kWh": "Compensation calculated automatically: kWh × €/kWh",
    "Conceptos adicionales": "Additional concepts", "ENERGÍA REACTIVA (€)": "REACTIVE ENERGY (€)", "EXCESO POTENCIA (€)": "POWER EXCESS (€)", "ALQUILER EQUIPOS (€)": "EQUIPMENT RENTAL (€)",
    "BONO SOCIAL / FINANCIACIÓN (€)": "SOCIAL BONUS / FINANCING (€)", "SERVICIO / OTROS (€)": "SERVICE / OTHERS (€)", "solo factura actual": "only current invoice",
    "Otros conceptos sujetos a IEE": "Other concepts subject to IEE", "+ Añadir concepto": "+ Add concept", "Siguiente → Comparativa": "Next → Comparison", "← Volver": "← Back",
    "Facturación actual": "Current billing", "Ranking de ofertas": "Offers ranking", "Oferta seleccionada": "Selected offer", "📄 Generar PDF para comercial": "📄 Generate PDF for agent",
    "Base de Datos de Ofertas": "Offers Database", "Tarifas disponibles · se guardan en archivo local": "Available tariffs · saved in local file", "+ Nueva Oferta": "+ New Offer",
    "🔑 API Key Anthropic": "🔑 Anthropic API Key", "API KEY": "API KEY", "Guardar API Key": "Save API Key", "🌐 Idioma": "🌐 Language", "IDIOMA DE LA INTERFAZ": "INTERFACE LANGUAGE",
    "👤 Gestión de Usuarios": "👤 User Management", "+ Nuevo usuario": "+ New user", "Cancelar": "Cancel", "Guardar": "Save", "Guardar Oferta": "Save Offer",
    "Comicionador": "Commissions", "Comercializadoras": "Suppliers", "Añadir Tramo": "Add Tier", "Guardar Cambios": "Save Changes", "Eliminar Empresa": "Delete Company",
    "Escalado de Comisiones (Tramos)": "Commission Tiers (Tiers)", "Selecciona una comercializadora para configurar sus comisiones.": "Select a supplier to configure its commissions.",
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
    "Datos del client": "Dades del client", "CLIENTE / RAZÓN SOCIAL": "CLIENT / RAÓ SOCIAL", "COMERCIALIZADORA ACTUAL": "COMERCIALITZADORA ACTUAL", "DIRECCIÓN": "ADREÇA", "CÓDIGO POSTAL": "CODI POSTAL", "TARIFA": "TARIFA",
    "Parámetros de facturación": "Paràmetres de facturació", "DÍAS FACTURADOS": "DIES FACTURATS", "FECHA INICIO PERÍODE": "DATA INICI PERÍODE", "TOTAL FACTURA (€) ⚠": "TOTAL FACTURA (€) ⚠",
    "IVA / IGIC (%)": "IVA / IGIC (%)", "IEE (%)": "IEE (%)", "IEE FACTURA ACTUAL (€)": "IEE FACTURA ACTUAL (€)", "IVA FACTURA ACTUAL (€)": "IVA FACTURA ACTUAL (€)", "DESCUENTO ENERGÍA ACTUAL (%)": "DESCOMPTE ENERGIA ACTUAL (%)",
    "Períodos de preu": "Períodes de preu", "Esta factura tiene 2 períodos de precio distintos": "Aquesta factura té 2 períodes de preu diferents",
    "Indica los días y precios de cada sub-período. La IA intentará extraerlos automáticamente.": "Indica els dies i preus. La IA intentarà extreure'ls automàticament.",
    "DÍAS PERÍODO 1": "DIES PERÍODE 1", "DÍAS PERÍODO 2": "DIES PERÍODE 2", "€/kWh PERÍODO 1 (P1)": "€/kWh PERÍODO 1 (P1)", "€/kWh PERÍODO 2 (P1)": "€/kWh PERÍODO 2 (P1)",
    "Término de potencia — P1 a P6": "Terme de potència — P1 a P6", "Término de energía — P1 a P6": "Terme d'energia — P1 a P6", "kW": "kW", "IMPORTE (€)": "IMPORT (€)", "kWh": "kWh", "€/kWh": "€/kWh",
    "Autoconsumo": "Autoconsum", "Esta factura tiene autoconsumo": "Aquesta factura té autoconsum", "kWh GENERADOS / COMPENSADOS": "kWh GENERATS / COMPENSATS",
    "€/kWh PRECIO COMPENSACIÓN ACTUAL": "€/kWh PREU COMPENSACIÓ ACTUAL", "TOTAL COMPENSACIÓN (€)": "TOTAL COMPENSACIÓ (€)", "La compensación se calculará automáticamente: kWh × €/kWh": "La compensació es calcularà automàticament: kWh × €/kWh",
    "Conceptos adicionales": "Conceptes addicionals", "ENERGÍA REACTIVA (€)": "ENERGIA REACTIVA (€)", "EXCESO POTENCIA (€)": "EXCÉS POTÈNCIA (€)", "ALQUILER EQUIPOS (€)": "LLOGUER EQUIPS (€)",
    "BONO SOCIAL / FINANCIACIÓN (€)": "BO SOCIAL / FINANÇAMENT (€)", "SERVICIO / OTROS (€)": "SERVEI / ALTRES (€)", "solo factura actual": "només factura actual",
    "Otros conceptos sujetos a IEE": "Altres conceptes subjectes a IEE", "+ Añadir concepto": "+ Afegir concepte", "Siguiente → Comparativa": "Següent → Comparativa", "← Volver": "← Tornar",
    "Facturación actual": "Facturació actual", "Ranking de ofertas": "Rànquing d'ofertes", "Oferta seleccionada": "Oferta seleccionada", "📄 Generar PDF para comercial": "📄 Generar PDF per a comercial",
    "Base de Datos de Ofertas": "Base de Dades d'Ofertes", "Tarifas disponibles · se guardan en archivo local": "Tarifes disponibles · Es guarden a l'arxiu local", "+ Nueva Oferta": "+ Nova Oferta",
    "🔑 API Key Anthropic": "🔑 API Key Anthropic", "API KEY": "API KEY", "Guardar API Key": "Desar API Key", "🌐 Idioma": "🌐 Idioma", "IDIOMA DE LA INTERFÍCIE": "IDIOMA DE LA INTERFÍCIE",
    "👤 Gestión de Usuarios": "👤 Gestió d'Usuaris", "+ Nuevo usuario": "+ Nou usuari", "Cancelar": "Cancel·lar", "Guardar": "Desar", "Guardar Oferta": "Desar Oferta",
    "Comisionado": "Comissionat", "Comercializadoras": "Comercialitzadores", "Añadir Tramo": "Afegir Tram", "Guardar Cambios": "Desar Canvis", "Eliminar Empresa": "Eliminar Empresa",
    "Escalado de Comisiones (Tramos)": "Escalat de Comissions (Trams)", "Selecciona una comercializadora para configurar les seves comissions.": "Selecciona una comercialitzadora per configurar les seves comissions.",
    "NOMBRE DE LA OFERTA": "NOM DE L'OFERTA", "COMERCIALIZADORA": "COMERCIALITZADORA", "TIPO DE PRECIO": "TIPUS DE PREU", "PERMANENCIA": "PERMANÈNCIA", "VALIDEZ (días)": "VALIDESA (dies)",
    "Rang d'aplicació": "Rang d'aplicació", "POT. MÍNIMA (kW)": "POT. MÍNIMA (kW)", "POT. MÁXIMA (kW)": "POT. MÀXIMA (kW)", "CONSUM MÍN. (kWh/any)": "CONSUM MÍN. (kWh/any)", "CONSUM MÀX. (kWh/any)": "CONSUM MÀX. (kWh/any)",
    "Comisión": "Comissió", "TIPO DE COMISIÓN": "TIPUS DE COMISSIÓ", "€ Fijo por contracte": "€ Fix per contracte", "Por consum (Coef. × kWh × FEE / 1000)": "Per consum",
    "COMISIÓN FIJA (€)": "COMISSIÓ FIXA (€)", "COEFICIENTE REPARTO (%)": "COEFICIENT REPARTIMENT (%)", "FEE (€/MWh)": "FEE (€/MWh)", "RESULTADO (se calcula automático)": "RESULTAT (es calcula automàticament)",
    "COMPENSACIÓN AUTOCONSUMO (€/kWh)": "COMPENSACIÓ AUTOCONSUM (€/kWh)", "DESCUENTO POTENCIA (%)": "DESCOMPTE POTÈNCIA (%)", "DESCUENTO ENERGÍA GLOBAL (%)": "DESCOMPTE ENERGIA GLOBAL (%)",
    "Discriminar dte. energia per període": "Discriminar dte. energia per període", "Precios de potencia (€/kW/día)": "Preus de potència (€/kW/dia)", "Precios de energía (€/kWh)": "Preus d'energia (€/kWh)",
    "NOMBRE": "NOM", "EMAIL": "EMAIL", "CONTRASEÑA": "CONTRASENYA", "(deixar buit per no canviar)": "(deixar buit per no canviar)", "PERFIL": "PERFIL",
    "Admin": "Admin", "Comercial": "Comercial", "Administración": "Administració",
    "Cargando...": "Carregant...", "Selecciona una oferta": "Selecciona una oferta", "Credenciales incorrectas": "Credencials incorrectes",

    // PDF SPECIFIC
    "ESTUDIO COMPARATIVO ENERGÉTICO": "ESTUDI COMPARATIU ENERGÈTIC", "Preparado el": "Preparat el", "Válido": "Vàlid per", "días": "dies",
    "OFERTA": "OFERTA", "TIPO": "TIPUS", "FACTURACIÓN ACTUAL": "FACTURACIÓ ACTUAL", "NUEVA FACTURACIÓN": "NOVA FACTURACIÓ",
    "T. FIJO — POTENCIA": "T. FIX — POTÈNCIA", "T. VARIABLE — ENERGÍA": "T. VARIABLE — ENERGIA", "OTROS CONCEPTOS": "ALTRES CONCEPTES", "IMPUESTOS Y OTROS": "IMPOSTOS I ALTRES",
    "TOTALS": "TOTALS", "TOTAL POTENCIA": "TOTAL POTÈNCIA", "TOTAL ENERGÍA": "TOTAL ENERGIA", "TOTAL": "TOTAL", "Base Imponible": "Base Imposable",
    "Compensación Autoconsum": "Compensació Autoconsum", "Energía Reactiva": "Energia Reactiva", "Alquiler Equipos": "Lloguer Equips",
    "Financiación Bono Social": "Finançament Bo Social", "Servicios": "Serveis", "Imp. Electricitat (IEE)": "Imp. Electricitat (IEE)",
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

  $('ui_nombre').textContent = ST.user.nombre;
  $('ui_role').textContent = ST.user.role==='admin' ? 'Admin' : 'Comercial';

  const isAdmin = ST.user.role === 'admin';
  $('tab-ofr').style.display = isAdmin ? '' : 'none';
  $('tab-com').style.display = isAdmin ? '' : 'none';

  await Promise.all([loadConfig(), loadOfertas(), loadUsuarios(), loadComisiones()]);

  // Load config into UI
  $('cfg_provider').value = ST.config.provider || 'anthropic';
  $('cfg_model').value = ST.config.model || '';
  $('cfg_apikey').value = '';
  $('cfg_apikey').placeholder = ST.config.has_api_key ? '*** API Key guardada ***' : 'sk-ant-...';
  $('cfg_geminikey').value = '';
  $('cfg_geminikey').placeholder = ST.config.has_gemini_key ? '*** Gemini Key guardada ***' : 'AIza...';
  $('cfg_openaikey').value = '';
  $('cfg_openaikey').placeholder = ST.config.has_openai_key ? '*** API Key guardada ***' : 'sk-...';
  $('cfg_openaiurl').value = ST.config.openai_url || 'https://api.openai.com/v1';
  $('cfg_idioma').value = ST.config.idioma||'es';

  uiTogIA();

  $('cfg-ia').style.display = isAdmin ? '' : 'none';
  $('cfg-users-addbar').style.display = isAdmin ? '' : 'none';

  $('g_asesor').value = localStorage.getItem('el_asesor')||'';
  const today = new Date().toISOString().split('T')[0];
  $('g_fecha').value = today;

  buildTbls();
  renderUsersTable();
  go('fac');
  applyLang();
}

function uiTogIA(){
  const p = $('cfg_provider').value;
  document.querySelectorAll('.ia-fields').forEach(el => el.style.display = 'none');
  $('ia_' + (p === 'groq' ? 'openai' : p)).style.display = 'block';
  
  // Optional: Set default models if empty
  const mod = $('cfg_model');
  if(!mod.value){
    if(p==='anthropic') mod.value = 'claude-3-5-sonnet-20241022';
    if(p==='google') mod.value = 'gemini-1.5-flash';
    if(p==='openai') mod.value = 'gpt-4o';
    if(p==='groq') mod.value = 'llama-3-70b-8192';
  }
}

// ════════════════════════════════════════════
// API CALLS
// ════════════════════════════════════════════
async function loadConfig(){
  try{ const r=await fetch('/api/config'); ST.config=await r.json(); } catch(e){}
}
async function saveConfig(){
  const p = $('cfg_provider').value;
  ST.config.provider = p;
  ST.config.idioma   = $('cfg_idioma').value;
  ST.config.model    = $('cfg_model').value.trim();
  
  const key_anth = $('cfg_apikey').value.trim();
  const key_gem  = $('cfg_geminikey').value.trim();
  const key_oa   = $('cfg_openaikey').value.trim();
  
  if(key_anth) ST.config.api_key = key_anth;
  if(key_gem)  ST.config.gemini_key = key_gem;
  if(key_oa)   ST.config.openai_key = key_oa;
  
  if(p === 'openai' || p === 'groq'){
    ST.config.openai_url = $('cfg_openaiurl').value.trim();
    if(p==='groq' && !ST.config.openai_url) ST.config.openai_url = 'https://api.groq.com/openai/v1';
  }

  await fetch('/api/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(ST.config)});
  
  if(key_anth) ST.config.has_api_key = true;
  if(key_gem)  ST.config.has_gemini_key = true;
  if(key_oa)   ST.config.has_openai_key = true;
  
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
  saveComsToServer();
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
    <td><button class="btn btn-d btn-sm" onclick="this.closest('tr').remove()">✕</button></td>
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
  tr.innerHTML='<td class="lbl">'+p+'</td><td><input type="number" id="pk_'+id+'" class="pk_in" step=".001" value="0"></td><td><input type="number" id="pi_'+id+'" class="pi_in" step=".01" value="0"></td><td><button class="btn btn-sm btn-d" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  $('potT').appendChild(tr);
}
function addEnL(per){
  const p=per||$('addEnSel').value; const id=enIdSeq++;
  const tr=document.createElement('tr'); tr.className='en-row'; tr.dataset.per=p;
  tr.innerHTML='<td class="lbl">'+p+'</td><td><input type="number" id="ek_'+id+'" class="ek_in" step=".001" value="0"></td><td><input type="number" id="ep_'+id+'" class="ep_in" step=".000001" value="0"></td><td><button class="btn btn-sm btn-d" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  $('enT').appendChild(tr);
}
function addLecL(per){
  const p=per||$('addLecSel').value; const id=lecIdSeq++;
  const tr=document.createElement('tr'); tr.className='lec-row'; tr.dataset.per=p;
  tr.innerHTML='<td class="lbl">'+p+'</td><td><input type="number" id="lk_'+id+'" class="lk_in" step=".001" value="0"></td><td><button class="btn btn-sm btn-d" onclick="this.closest(\'tr\').remove()">✕</button></td>';
  $('lecT').appendChild(tr);
}

function updTar(){
  const v = n($('f_pot').value);
  const currentTar = $('f_tar').value;
  let t = v<=15?'2.0TD':'3.0TD';
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

function syncTarCups(v){
  $('f_tar').value=v;
  $('f_tar_cups').value=v;
  $('tarTag').textContent=v;
  $('potHint').style.display = v!=='2.0TD'?'block':'none';
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
if(uz){
  uz.addEventListener('dragover',function(e){e.preventDefault();uz.style.borderColor='var(--acc)';});
  uz.addEventListener('dragleave',function(){uz.style.borderColor='';});
  uz.addEventListener('drop',function(e){e.preventDefault();uz.style.borderColor='';onFiles(e.dataTransfer.files);});
}

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
  const p = ST.config.provider || 'anthropic';
  const hasKey = (p==='anthropic' && ST.config.has_api_key) || 
                 (p==='google' && ST.config.has_gemini_key) || 
                 ((p==='openai'||p==='groq') && ST.config.has_openai_key);

  if(!hasKey){sb('Configura la API Key para ' + p.toUpperCase() + ' en Configuración','err'); return;}
  if(!ST.files.length){sb('Sube al menos un archivo','err');return;}
  $('btnEx').disabled=true; sb('Analizando factura con IA ('+p.toUpperCase()+')…','load');

  // ... (Prompt stays same)
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
    const resp=await fetch('/api/extract',{
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
  
  if(d.tiene_autoconsumo){
    $('f_tiene_autocon').checked=true; togAutocon();
    set('f_aut_kwh',d.autoconsumo_kwh,'alta');
    set('f_aut_precio',d.autoconsumo_precio_kwh,'alta');
    set('f_aut_total',d.autoconsumo_total,'alta');
  }
  
  if(d.tiene_multiples_periodos){
    $('f_dos_periodos').checked=true; togDosPeriodos();
  } else {
    $('f_dos_periodos').checked=false; togDosPeriodos();
  }
  
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
    PS.forEach(p=>{
      const total=enArr.filter(e=>e.per===p).reduce((s,e)=>s+n(e.kwh),0);
      addLecL(p); const id=lecIdSeq-1;
      $('lk_'+id).value=total>0?total:0;
    });
  }

  if(maxKw>0) d.potencia_kw = maxKw;
  $('f_pot_cups').value=d.potencia_kw||'';
  
  let tarFinal = '';
  if(d.tarifa && ['2.0TD', '3.0TD', '6.1TD'].includes(d.tarifa.toUpperCase())) {
     tarFinal = d.tarifa.toUpperCase();
  } else {
     const tv=n(d.potencia_kw);
     tarFinal = tv<=15?'2.0TD':'3.0TD';
     if(tv > 150) tarFinal = '6.1TD'; 
  }
  
  $('f_tar').value=tarFinal;
  $('f_tar_cups').value=tarFinal;
  updTar();
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
  const i1=document.createElement('input'); i1.type='text'; i1.placeholder='Ej: Ajust Restriccions'; i1.value=nombre; i1.style.cssText='background:var(--bg);border:1px solid var(--b1);border-radius:6px;padding:7px 10px;color:var(--tx);font-family:monospace;font-size:12px;width:100%';
  const i2=document.createElement('input'); i2.type='number'; i2.step='.01'; i2.placeholder='€'; i2.value=importe||''; i2.style.cssText='background:var(--bg);border:1px solid var(--b1);border-radius:6px;padding:7px 10px;color:var(--tx);font-family:monospace;font-size:12px;text-align:right;width:100%';
  const lbl=document.createElement('label'); lbl.style.cssText='display:flex;align-items:center;gap:5px;font-size:10px;color:var(--t2);cursor:pointer;white-space:nowrap';
  const chk=document.createElement('input'); chk.type='checkbox'; chk.checked=mantiene; chk.style.accentColor='var(--acc)';
  lbl.appendChild(chk); lbl.appendChild(document.createTextNode(' En nueva'));
  const btn=document.createElement('button'); btn.className='btn btn-d btn-sm'; btn.textContent='✕'; btn.onclick=function(){document.getElementById(id).remove();};
  div.appendChild(i1); div.appendChild(i2); div.appendChild(lbl); div.appendChild(btn);
  $('ieeExtras').appendChild(div);
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
  const hasLecturas = lecArr.some(l=>l.kwh>0);
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
  const slug = clean(oferta.comercializadora);
  const regla = ST.comisiones.find(c => clean(c.comercializadora) === slug);
  
  if(regla && regla.tramos && regla.tramos.length){
    const ofrName = clean(oferta.nombre);
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
  const potByPer={};
  PS.forEach(p=>{potByPer[p]={kw:0}});
  d.pot_p.forEach(l=>{ if(potByPer[l.per] && l.kw>potByPer[l.per].kw) potByPer[l.per].kw=l.kw; });

  const simByPer = d.lec_by_per || {};
  const totalKwh = PS.reduce((s,p)=>s+(simByPer[p]||0), 0);

  let tPot=0;
  PS.forEach(p=>{
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
  if(cAct && cOfr && cAct === cOfr) return false;
  const isIbe = cAct.includes('iberdrola') || cOfr.includes('iberdrola');
  const isNib = cAct.includes('niba') || cOfr.includes('niba');
  if(isIbe && isNib) return false;
  const isExxi = cAct.includes('energia xxi') || cOfr.includes('energia xxi');
  const isEnd = cAct.includes('endesa') || cOfr.includes('endesa');
  if(isExxi && isEnd) return false;
  if(o.tarifa!=='todas' && o.tarifa!==d.tarifa) return false;
  const pot=d.potencia_kw;
  if(pot<(o.pot_min||0) || pot>(o.pot_max||9999)) return false;
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
    +'<div class="trow"><span class="trow-l">Impuesto Eléctrico (IEE) (extraído)</span><span>'+(d.iee_act||0).toFixed(2)+' €</span></div>'
    +(servSum>0?'<div class="trow"><span class="trow-l">Servicios extra</span><span>'+servSum.toFixed(2)+' €</span></div>':'')
    +'<div class="trow"><span class="trow-l">IVA ('+d.iva_pct+'%)</span><span>'+ivaActCalc.toFixed(2)+' €</span></div>'
    +'<div class="trow" style="margin-bottom:0"><span class="trow-l" style="color:var(--tx);font-weight:600">TOTAL FACTURA</span>'
    +'<span style="font-size:19px;font-weight:800;font-family:\'Syne\',sans-serif">'+calcTotalAct.toFixed(2)+' €</span></div>';

  const ofertasFiltradas=ST.ofertas.filter(function(o){return ofertaMatchesFact(o,d);});
  if(!ofertasFiltradas.length){
    $('rankDiv').innerHTML='<div class="empty"><div class="eico">⚡</div>'
      +(ST.ofertas.length===0?'No hay ofertas en la base de datos.':'No hay ofertas compatibles.')+'</div>';
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
  let display=res;
  if(!isAdmin){
    const con7=res.filter(function(r){return r.ahorroPct>=7;});
    if(con7.length>0) display=[con7[0]];
    else {
      const conAhorro=res.filter(function(r){return r.ahorro>0;});
      if(conAhorro.length>0) display=[conAhorro[0]];
      else {
        $('rankDiv').innerHTML='<div class="no-oferta"><div style="font-size:24px;margin-bottom:8px">ℹ️</div><div style="font-weight:700">De momento no hay una oferta mejor</div></div>';
        return;
      }
    }
  }

  $('rankDiv').innerHTML=display.map(function(r,i){
    const badge = i === 0 ? '<span class="bdg bdg-g">✨ Recomendada</span>' : '';
    const isSelected = ST.sel?.id === r.id;
    return '<div class="ofr-card anim-in ' + (i === 0 ? 'top' : '') + ' ' + (isSelected ? 'sel' : '') + '" onclick="selOfr(\'' + r.id + '\')" style="animation-delay:'+(i*0.05)+'s">'
      + '<div style="display:flex;justify-content:space-between;margin-bottom:12px">'
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
  const d=getForm(), isAdmin=ST.user?.role==='admin';
  $('detDiv').innerHTML='<div class="card anim-in" style="margin-bottom:0">'
    +'<div class="ct">Detalles de la Oferta</div>'
    +'<div style="font-family:\'Outfit\',sans-serif;font-weight:700;font-size:18px;margin-bottom:4px">'+r.nombre+'</div>'
    +'<div style="color:var(--t2);font-size:12px;margin-bottom:20px">'+r.comercializadora+' · '+r.tipo+'</div>'
    +'<div class="trow"><span class="trow-l">Potencia</span><span>'+r.tPot.toFixed(2)+' €</span></div>'
    +'<div class="trow"><span class="trow-l">Energía</span><span>'+r.tEn.toFixed(2)+' €</span></div>'
    +(r.compNva>0?'<div class="trow"><span class="trow-l">Compensación Autoconsumo</span><span style="color:var(--ok)">-'+r.compNva.toFixed(2)+' €</span></div>':'')
    +'<div class="trow"><span class="trow-l">Impuesto Eléctrico</span><span>'+r.iee.toFixed(2)+' €</span></div>'
    +'<div class="trow"><span class="trow-l">IVA</span><span>'+r.iva.toFixed(2)+' €</span></div>'
    +'<div class="trow" style="margin-top:12px;background:rgba(255,255,255,0.05)"><span class="trow-l" style="font-weight:700">TOTAL ESTIMADO</span><span style="font-size:20px;color:var(--acc)">'+r.total.toFixed(2)+' €</span></div>'
    +'<div class="ahorro-box">'
      +'<div><div style="font-weight:700;color:var(--ok)">AHORRO ESTIMADO</div>'
      +'<div style="font-size:11px;color:var(--ok)">Anual: ~'+r.ahorroAnual.toFixed(0)+' €</div></div>'
      +'<div class="ahorro-v">'+(r.ahorro>=0?'+':'')+r.ahorro.toFixed(2)+' €</div>'
    +'</div>'
    +(isAdmin?'<div class="com-box"><div style="font-size:10px;font-weight:700">Comisión</div><div class="com-v">'+r.comision.toFixed(2)+' €</div></div>':'')
    +'</div>';
}

function genPDF(){
  if(!ST.sel){alert('Selecciona una oferta primero');return;}
  const d=getForm(), r=ST.sel;
  const asesor=($('g_asesor')?.value||'').trim();
  const fechaProp=$('g_fecha')?.value||new Date().toISOString().split('T')[0];
  const validezDias=r.validez||7;
  const fechaFmt=iso=>{if(!iso)return'';const p=iso.split('-');return p[2]+'/'+p[1]+'/'+p[0];};
  const fmt=v=>v===0?'— €':v.toFixed(2)+' €';
  const fmtP=v=>v===0?'—':v.toFixed(5);
  const servSum=d.servicio||0;
  const baseIVAAct=(d.total_factura-d.iva_act)+servSum;
  const ivaActCalc=d.iva_act+(servSum*(d.iva_pct/100));
  const calcTotalAct=baseIVAAct+ivaActCalc;
  
  const ahorroEur=calcTotalAct-r.total;
  const ahorroPct=calcTotalAct>0?(ahorroEur/calcTotalAct*100):0;
  const ahorroAnual=d.dias>0?(ahorroEur/d.dias*365):0;
  const tPotAct=d.pot_p.reduce((s,l)=>s+l.importe,0);
  const dtoActPct=d.dto_en_act_pct||0, ieeAct=d.iee_act||0, ivaAct=ivaActCalc;
  const dtoEnNvaPct=r.dto_energia_por_periodo?0:(r.dto_energia_global||0);
  let tEnNvaBase=0, tEnActBase=0, rowsPot='', rowsEn='';
  
  PS.forEach(p=>{
    const pLines=d.pot_p.filter(x=>x.per===p), kwNva=pLines.length>0?Math.max(...pLines.map(x=>x.kw)):0;
    let ppNva=r['pp_'+p.toLowerCase()]||0;
    if(d.tarifa.startsWith('2.0')&&p==='P3'&&!ppNva) ppNva=r.pp_p2||0;
    const impNva=kwNva*ppNva*d.dias;
    if(pLines.length===0) rowsPot+='<tr><td class="per">'+p+'</td><td class="num">—</td><td class="num">—</td><td class="num bold">— €</td><td class="sep"></td><td class="num">—</td><td class="num">'+fmtP(ppNva)+'</td><td class="num bold nva">— €</td></tr>';
    else pLines.forEach((l,i)=>{
      const prAct=(l.kw>0&&d.dias>0)?l.importe/(l.kw*d.dias):0;
      rowsPot+='<tr><td class="per">'+(i===0?p:'')+'</td><td class="num">'+(l.kw>0?l.kw.toFixed(3):'—')+'</td><td class="num">'+fmtP(prAct)+'</td><td class="num bold">'+(l.importe>0?fmt(l.importe):'— €')+'</td><td class="sep"></td><td class="num">'+(i===0&&kwNva>0?kwNva.toFixed(3):'')+'</td><td class="num">'+(i===0?fmtP(ppNva):'')+'</td><td class="num bold nva">'+(i===0&&impNva>0?fmt(impNva):'')+'</td></tr>';
    });
  });

  const simByPer=d.lec_by_per||{};
  PS.forEach((p,idx)=>{
    const eLines=d.en_p.filter(x=>x.per===p), dtoP=r.dto_energia_por_periodo?(r['dto_e_p'+(idx+1)]||0)/100:dtoEnNvaPct/100;
    const epNva=r['ep_'+p.toLowerCase()]||0, kwhSim=simByPer[p]||0, impNvaSim=kwhSim*epNva*(1-dtoP);
    tEnNvaBase+=kwhSim*epNva;
    if(eLines.length===0&&kwhSim===0) rowsEn+='<tr><td class="per">'+p+'</td><td class="num">—</td><td class="num">—</td><td class="num bold">— €</td><td class="sep"></td><td class="num">—</td><td class="num">'+fmtP(epNva)+'</td><td class="num bold nva">— €</td></tr>';
    else if(eLines.length===0&&kwhSim>0) rowsEn+='<tr><td class="per">'+p+'</td><td class="num">—</td><td class="num">—</td><td class="num bold">— €</td><td class="sep"></td><td class="num">'+kwhSim.toFixed(3)+'</td><td class="num">'+fmtP(epNva)+'</td><td class="num bold nva">'+fmt(impNvaSim)+'</td></tr>';
    else eLines.forEach((l,i)=>{
      const impAB=l.kwh*l.precio; tEnActBase+=impAB;
      rowsEn+='<tr><td class="per">'+(i===0?p:'')+'</td><td class="num">'+(l.kwh>0?l.kwh.toFixed(3):'—')+'</td><td class="num">'+(l.precio>0?fmtP(l.precio):'—')+'</td><td class="num bold">'+(impAB>0?fmt(impAB):'— €')+'</td><td class="sep"></td>';
      if(i===0) rowsEn+='<td class="num">'+(kwhSim>0?kwhSim.toFixed(3):'—')+'</td><td class="num">'+(epNva>0?fmtP(epNva):'—')+'</td><td class="num bold nva">'+(impNvaSim>0?fmt(impNvaSim):'— €')+'</td>';
      else rowsEn+='<td class="num"></td><td class="num"></td><td class="num bold nva"></td>';
      rowsEn+='</tr>';
    });
  });

  const dtoActEur=tEnActBase*(dtoActPct/100), tEnActNeto=tEnActBase-dtoActEur, dtoNvaEur=tEnNvaBase*(dtoEnNvaPct/100);
  let rowsExtras='';
  if((d.iee_extras||[]).length>0){
    rowsExtras+='<tr><td colspan="8" class="sec-hdr">OTROS CONCEPTOS</td></tr>';
    d.iee_extras.forEach(e=>{rowsExtras+='<tr><td colspan="3" style="padding:4px 8px">'+e.nombre+'</td><td class="num bold">'+fmt(e.importe)+'</td><td class="sep"></td><td colspan="2"></td><td class="num bold nva">'+(e.mantiene?fmt(e.importe):'— €')+'</td></tr>';});
  }
  const autActEur=d.tiene_autoconsumo?(d.autoconsumo_kwh||0)*(d.autoconsumo_precio_kwh||0):0, autNvaEur=r.compNva||0;
  const logoSVG='<svg width="110" height="52" viewBox="0 0 110 52" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="13" r="12" fill="#3d4044"/><text x="14" y="18" text-anchor="middle" fill="white" font-size="10" font-family="Arial" font-weight="bold">G</text><circle cx="14" cy="39" r="12" fill="#2cb5ad"/><text x="14" y="44" text-anchor="middle" fill="white" font-size="10" font-family="Arial" font-weight="bold">G</text><text x="32" y="18" font-family="Arial" font-size="12" font-weight="900" fill="#3d4044">GESTION</text><text x="32" y="33" font-family="Arial" font-size="12" font-weight="900" fill="#3d4044">GROUP</text><text x="32" y="48" font-family="Arial" font-size="6.5" fill="#2cb5ad" letter-spacing="2">SOLUCIONES ENERGÉTICAS</text></svg>';
  const w=window.open('','_blank');
  w.document.write('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:Arial,sans-serif;font-size:10.5px;color:#2d3138;padding:16px 20px}.hdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;padding-bottom:9px;border-bottom:3px solid #2cb5ad}.hdr-right{text-align:right;font-size:9.5px;color:#6b7280;line-height:1.6}.hdr-right b{font-size:11px;color:#2d3138}.offer-bar{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;background:#f0fafb;border:1px solid #b2e0de;border-radius:6px;padding:7px 10px;margin-bottom:9px;font-size:9.5px}.offer-bar .lbl{color:#6b7280;margin-bottom:1px}.offer-bar .val{font-weight:800;font-size:10.5px}.offer-bar .val.teal{color:#2cb5ad}table{width:100%;border-collapse:collapse;font-size:9.5px}.th-act{background:#3d4044;color:#fff;padding:4px 7px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;text-align:center}.th-nva{background:#2cb5ad;color:#fff;padding:4px 7px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;text-align:center}.sec-hdr{background:#f3f4f6;color:#3d4044;padding:4px 7px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #e5e7eb}.col-hdr{background:#f9fafb;color:#374151;padding:3px 7px;font-size:8.5px;font-weight:600;text-align:center;border-bottom:1px solid #e5e7eb}.per{padding:3px 7px;border-bottom:1px solid #f3f4f6;color:#2cb5ad;font-weight:700;width:26px;text-align:center}.num{padding:3px 7px;border-bottom:1px solid #f3f4f6;text-align:right}.num.bold{font-weight:700}.num.nva{background:#f0fafb}.sep{width:5px;background:#e5e7eb;padding:0}.dto-row td{padding:2px 7px;border-bottom:1px solid #e5e7eb;font-size:8.5px;color:#6b7280;font-style:italic}.dto-row .red{color:#dc2626;font-style:normal}.tot-row td{background:#f9fafb;font-weight:700;font-size:10.5px;padding:4px 7px;border-top:2px solid #d1d5db;border-bottom:1px solid #e5e7eb}.tot-row .nva{background:#e6f7f6;color:#1a7a75}.ext-row td{padding:3px 7px;border-bottom:1px solid #f3f4f6}.ext-row .nva{background:#f0fafb}.ahorro{background:linear-gradient(135deg,#e6f7f6,#d1f0ee);border:2px solid #2cb5ad;border-radius:7px;padding:11px 16px;display:flex;justify-content:space-between;align-items:center;margin:10px 0}.ahorro-lbl{font-weight:800;color:#1a7a75;font-size:11px}.ahorro-sub{font-size:9.5px;color:#2cb5ad;margin-top:2px}.ahorro-val .eur{font-size:22px;font-weight:900;color:#1a7a75;text-align:right}.ahorro-val .pct{font-size:13px;font-weight:700;color:#2cb5ad;text-align:right}.it{width:100%;border-collapse:collapse;margin-bottom:9px}.it th{background:#f3f4f6;padding:4px 9px;font-size:8.5px;font-weight:700;text-align:left;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #e5e7eb}.it td{padding:4px 9px;border-bottom:1px solid #f3f4f6;font-size:10px}.footer-bar{display:flex;justify-content:space-between;align-items:flex-end;margin-top:10px;padding-top:8px;border-top:2px solid #2cb5ad}.asesor-box{background:#f0fafb;border:1px solid #b2e0de;border-radius:6px;padding:7px 14px}.asesor-lbl{font-size:8px;color:#6b7280;text-transform:uppercase}.asesor-name{font-size:12px;font-weight:800}.foot-legal{font-size:8px;color:#9ca3af;text-align:right}@media print{body{padding:8px 12px}@page{margin:7mm}}</style></head><body>'
+'<div class="hdr"><div><div>'+logoSVG+'</div><div style="font-size:16px;font-weight:900">'+t('ESTUDIO COMPARATIVO ENERGÉTICO')+'</div><div>'+t('Preparado el')+' '+fechaFmt(fechaProp)+' · '+t('Válido')+' '+validezDias+' días</div></div><div class="hdr-right"><b>'+(d.cliente||'')+'</b><br>'+(d.cups||'')+'<br>'+d.tarifa+'</div></div>'
+'<div class="offer-bar"><div><div class="lbl">'+t('COMERCIALIZADORA ACTUAL')+'</div><div class="val">'+(d.comercializadora||'—')+'</div></div><div><div class="lbl">OFERTA</div><div class="val teal">'+r.nombre+'</div></div></div>'
+'<table><thead><tr><td colspan="4" class="th-act">'+t('FACTURACIÓN ACTUAL')+'</td><td class="sep"></td><td colspan="3" class="th-nva">'+t('NUEVA FACTURACIÓN')+'</td></tr></thead>'
+'<tbody>'+rowsPot+'<tr class="tot-row"><td colspan="3">POTENCIA</td><td class="num">'+fmt(tPotAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.tPot)+'</td></tr>'
+'<tr><td colspan="8" class="sec-hdr">ENERGÍA</td></tr>'+rowsEn+'<tr class="tot-row"><td colspan="3">ENERGÍA</td><td class="num">'+fmt(tEnActNeto)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.tEn)+'</td></tr>'
+rowsExtras+'<tr><td colspan="8" class="sec-hdr">IMPUESTOS Y OTROS</td></tr>'
+(d.tiene_autoconsumo?'<tr class="ext-row"><td colspan="3">Autoconsumo</td><td class="num">-'+fmt(autActEur)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">-'+fmt(autNvaEur)+'</td></tr>':'')
+'<tr class="ext-row"><td colspan="3">Imp. Electricidad</td><td class="num">'+fmt(ieeAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.iee)+'</td></tr>'
+'<tr class="ext-row"><td colspan="3">IVA</td><td class="num">'+fmt(ivaAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.iva)+'</td></tr>'
+'<tr class="tot-row"><td colspan="3">TOTAL</td><td class="num">'+fmt(calcTotalAct)+'</td><td class="sep"></td><td colspan="2"></td><td class="num nva">'+fmt(r.total)+'</td></tr></tbody></table>'
+'<div class="ahorro"><div><div class="ahorro-lbl">AHORRO ESTIMADO</div><div class="ahorro-sub">Anual: '+ahorroAnual.toFixed(0)+' €</div></div><div class="ahorro-val"><div class="eur">'+fmt(ahorroEur)+'</div><div class="pct">'+ahorroPct.toFixed(2)+'%</div></div></div>'
+'<div class="footer-bar"><div class="asesor-box"><div class="asesor-lbl">Asesor</div><div class="asesor-name">'+(asesor||'—')+'</div></div><div class="foot-legal">Precios incluyen peajes. Cálculos informativos.</div></div></body></html>');
  w.document.close(); setTimeout(()=>w.print(),700);
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
    const o=ST.ofertas.find(x=>x.id===id);
    $('modOfrT').textContent='Editar Oferta';
    const map={nom:'nombre',com:'comercializadora',tar:'tarifa',tip:'tipo',per:'permanencia',val:'validez',pmin:'pot_min',pmax:'pot_max',cmin:'consumo_min',cmax:'consumo_max',tco:'tipo_comision',co:'comision',coef:'coef_reparto',fee:'fee_mwh',comp:'compensacion',dp:'dto_potencia',de:'dto_energia_global',pp1:'pp_p1',pp2:'pp_p2',pp3:'pp_p3',pp4:'pp_p4',pp5:'pp_p5',pp6:'pp_p6',ep1:'ep_p1',ep2:'ep_p2',ep3:'ep_p3',ep4:'ep_p4',ep5:'ep_p5',ep6:'ep_p6',de1:'dto_e_p1',de2:'dto_e_p2',de3:'dto_e_p3',de4:'dto_e_p4',de5:'dto_e_p5',de6:'dto_e_p6'};
    flds.forEach(f=>{const el=$('o_'+f);if(el&&o[map[f]]!==undefined)el.value=o[map[f]];});
    $('o_dpp').checked=!!o.dto_energia_por_periodo;
  } else {
    $('modOfrT').textContent='Nueva Oferta';
    flds.forEach(f=>{const el=$('o_'+f);if(el)el.value='';});
    $('o_val').value=7;$('o_pmin').value=0;$('o_pmax').value=9999;$('o_cmin').value=0;$('o_cmax').value=99999999;
    $('o_dp').value=0;$('o_de').value=0;$('o_comp').value=0;$('o_tco').value='fijo';$('o_dpp').checked=false;
  }
  togDpp();togComision();
  $('modalOfr').style.display='flex'; document.body.style.overflow='hidden';
}
function closeMod(id){$(id).style.display='none'; document.body.style.overflow='';}

function saveOfr(){
  const nom=$('o_nom').value.trim(); if(!nom){alert('Nombre obligatorio');return;}
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
  if(ST.editOfrId){const i=ST.ofertas.findIndex(x=>x.id===ST.editOfrId);ST.ofertas[i]=o;}
  else ST.ofertas.push(o);
  saveOfertasToServer(); updCnt(); closeMod('modalOfr'); renderOfrList();
  applyLang();
}
function delOfr(id){
  if(!confirm('¿Eliminar oferta?'))return;
  ST.ofertas=ST.ofertas.filter(x=>x.id!==id);
  saveOfertasToServer(); updCnt(); renderOfrList();
  applyLang();
}
function renderOfrList(){
  const el=$('ofrList');
  if(!ST.ofertas.length){el.innerHTML='<div class="empty">No hay ofertas.</div>';return;}
  el.innerHTML=ST.ofertas.map((o, i)=>'<div class="card anim-in"><b>'+o.nombre+'</b><br>'+o.comercializadora+'<button onclick="openMod(\''+o.id+'\')">✎</button></div>').join('');
}

// ════════════════════════════════════════════
// USUARIOS
// ════════════════════════════════════════════
function renderUsersTable(){
  const isAdmin=ST.user?.role==='admin';
  const users=isAdmin?ST.usuarios:ST.usuarios.filter(u=>u.id===ST.user?.id);
  if(!users.length) return;
  $('cfg-users-content').innerHTML='<table class="users-table"><thead><tr><th>Nombre</th><th>Email</th><th></th></tr></thead><tbody>'
    +users.map(u=>'<tr><td>'+u.nombre+'</td><td>'+u.email+'</td><td><button onclick="openUserMod(\''+u.id+'\')">✎</button></td></tr>').join('')+'</tbody></table>';
}

function openUserMod(id){
  ST.editUserId=id;
  if(id){
    const u=ST.usuarios.find(x=>x.id===id);
    $('u_nombre').value=u.nombre; $('u_email').value=u.email;
  }
  $('modalUser').style.display='flex';
}
async function saveUser(){
  const nombre=$('u_nombre').value, email=$('u_email').value, pass=$('u_pass').value, role=$('u_role').value;
  await fetch('/api/usuarios',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:ST.editUserId?'update':'create',id:ST.editUserId,nombre,email,password:pass,role})});
  await loadUsuarios(); renderUsersTable(); closeMod('modalUser');
}
