import requests

url = "https://comparador-gestion-group-eight.vercel.app/api/extract-pdf"

# Create a minimal valid PDF
pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> >>\nendobj\n4 0 obj\n<< /Length 53 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Factura de Prueba 100 EUR) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000288 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n392\n%%EOF"

# Need an API key since the endpoint requires it. We know the master key or we can just pass the one we know.
# Wait, Vercel reads the API key from the database if we pass a valid session key. But we don't have a session key.
# However, MASTER_API_KEY might be set. Or we can just use the openai key as X-API-KEY if it's the master key?
# Actually, the user logged in, so they have a session.
# If we don't pass X-API-KEY, it will return 401 Unauthorized. Let's see what 401 returns.

response = requests.post(
    url,
    files={"file": ("test.pdf", pdf_content, "application/pdf")}
)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text!r}")
