
import uvicorn
import os
import sys
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.index import app
import json

# --- AUTO-DETECT FIREBASE KEY ---
firebase_key_path = None
for f in os.listdir("."):
    if f.endswith(".json") and "firebase-adminsdk" in f:
        firebase_key_path = f
        break

if firebase_key_path:
    print(f"✅ Llave de Firebase detectada: {firebase_key_path}")
    with open(firebase_key_path, 'r') as jf:
        os.environ["FIREBASE_SERVICE_ACCOUNT"] = jf.read()
else:
    print("⚠️ ADVERTENCIA: No se encontró la llave de Firebase (*.json).")
    print("Para que funcione el Login e Historial, descarga la llave de Firebase Console y ponla en esta carpeta.")

# Montar la carpeta public para servir el frontend
public_path = os.path.join(os.getcwd(), "public")
if os.path.exists(public_path):
    app.mount("/", StaticFiles(directory=public_path, html=True), name="public")
else:
    print(f"Error: No se encontró la carpeta 'public' en {public_path}")

@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    # Para SPA: redirigir 404 al index.html
    return FileResponse(os.path.join(public_path, "index.html"))

if __name__ == "__main__":
    print("--- INICIANDO SERVIDOR LOCAL GESTION GROUP ---")
    print("Abre tu navegador en: http://localhost:3000")
    uvicorn.run("run_local:app", host="0.0.0.0", port=3000, reload=True)
