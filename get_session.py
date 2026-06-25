import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

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
sessions = db.collection('_sessions').limit(1).get()
for s in sessions:
    print(f"API_KEY: {s.id}")
