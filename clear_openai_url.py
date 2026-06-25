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
doc_ref = db.collection('config').document('global')
doc_ref.update({
    'openai_url': ''
})
print("openai_url cleared.")
