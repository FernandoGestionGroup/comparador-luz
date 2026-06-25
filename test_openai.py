import sys
import os

# Agregamos la ruta actual para poder importar api.index
sys.path.append(os.getcwd())

from api.index import extraer_datos_factura

texto = "Factura de luz de prueba. Cliente: Juan Perez. Total: 100 EUR. CUPS: ES00112233445566778899"
keys = {
    "openai": "sk-proj-TU_API_KEY_AQUI"
}

print("Llamando a extraer_datos_factura con OpenAI...")
try:
    resultado = extraer_datos_factura(texto, keys, "openai")
    print("Éxito!")
    print(resultado)
except Exception as e:
    print("Error lanzado por la función:", e)
