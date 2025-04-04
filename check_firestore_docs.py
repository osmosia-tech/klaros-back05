from firestone_bridge4 import db
from dotenv import load_dotenv
import os
load_dotenv()

print("🧾 Listing brut des documents (sans filtre)")

try:
    docs = db.collection("conversations").limit(5).get()
    print(f"✅ Total docs récupérés : {len(docs)}")
    for doc in docs:
        print("-", doc.to_dict())
except Exception as e:
    print("❌ Erreur brut Firestore :", e)

