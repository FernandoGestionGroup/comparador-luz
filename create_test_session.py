import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
import time

key_path = None
for f in os.listdir("."):
    if f.endswith(".json") and "firebase-adminsdk" in f:
        key_path = f
        break

if key_path:
    with open(key_path, 'r') as jf:
        creds_dict = json.load(jf)
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = firestore.client()

api_key = "test_session_12345"
db.collection('_sessions').document(api_key).set({
    "id": "admin_test",
    "role": "admin",
    "nombre": "Test Admin",
    "created_at": time.time()
})
print("Creada sesión de prueba: test_session_12345")
