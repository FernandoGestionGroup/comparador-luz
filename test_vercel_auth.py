import requests
import sys

url = "https://comparador-gestion-group-eight.vercel.app/api/extract-pdf"
api_key = "test_session_12345"

pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> >>\nendobj\n4 0 obj\n<< /Length 214 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Factura Electrica Comercializadora SA 2026-06-23 Juan Perez Garcia CUPS: ES0021000000000000AA1F Tarifa 2.0TD Potencia P1: 3.3 kW P2: 3.3 kW Consumo Energia P1: 100 kWh P2: 50 kWh P3: 20 kWh Total: 120.50 EUR) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000288 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n392\n%%EOF"

headers = {
    "X-API-KEY": api_key,
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

print("Enviando petición a Vercel...")
response = requests.post(
    url,
    headers=headers,
    files={"file": ("test.pdf", pdf_content, "application/pdf")}
)

print(f"Status Code: {response.status_code}")
print("Headers:")
for k, v in response.headers.items():
    print(f"  {k}: {v}")

print("\nRaw Body Preview (first 100 bytes):")
print(repr(response.content[:100]))

if response.status_code == 200:
    try:
        print("\nJSON parseado con éxito:")
        print(response.json())
    except Exception as e:
        print(f"\nFallo al parsear JSON: {e}")
