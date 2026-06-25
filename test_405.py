import requests

url = "https://comparador-gestion-group-eight.vercel.app/api/extract-pdf"

# We'll just do a GET request to see if Vercel returns something weird on Method Not Allowed
# Or just upload the same PDF but see if it fails.
response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Body: {response.text[:200]}")
