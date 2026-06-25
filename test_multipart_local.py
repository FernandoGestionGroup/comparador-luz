import requests

try:
    print("Enviando POST multipart...")
    res = requests.post(
        "http://localhost:3000/api/extract-pdf", 
        files={"file": open("test_large.pdf", "rb")},
        headers={"X-API-KEY": "test_session_12345"}
    )
    print(f"Status: {res.status_code}")
    print(res.text)
except Exception as e:
    print(f"Error: {e}")
