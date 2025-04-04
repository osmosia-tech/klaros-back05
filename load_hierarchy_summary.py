# load_hierarchy_summary.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialisation Firebase
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def load_hierarchy_summary(user_id, limit=5):
    db = firestore.client()

    # Requête brute sans tri complexe (sans order_by)
    all_docs = db.collection("conversation_summaries_hierarchy") \
                 .where("user_id", "==", user_id) \
                 .get()

    # Extraction + tri côté Python
    filtered = []
    for doc in all_docs:
        data = doc.to_dict()
        if "chunk_index" in data and "text" in data:
            filtered.append(data)

    # Tri local
    filtered.sort(key=lambda x: x["chunk_index"])
    top = filtered[:limit]

    print(f"[SUMMARY] {len(top)} blocs hiérarchiques récupérés")

    return [
        {"role": "system", "content": f"[Résumé bloc {i+1}] {s['text']}"}
        for i, s in enumerate(top)
    ]
