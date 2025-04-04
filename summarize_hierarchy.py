import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from openai import OpenAI

# Initialisation
load_dotenv()
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

USER_ID = "elias_klaros"
BLOCK_SIZE = 10  # Nombre de messages par bloc résumé

# Étape 1 : Récupérer tous les messages utilisateur/assistant
docs = (
    db.collection("conversations")
    .where("user_id", "==", USER_ID)
    .order_by("timestamp")
    .get()
)

logging.info(f"[HIERARCHY] {len(docs)} messages récupérés pour {USER_ID}")

messages = []
for doc in docs:
    d = doc.to_dict()
    messages.append({
        "role": d.get("role", "user"),
        "content": d.get("message", ""),
        "timestamp": d.get("timestamp")
    })

# Étape 2 : Créer des blocs et générer un résumé par bloc
blocks = [messages[i:i+BLOCK_SIZE] for i in range(0, len(messages), BLOCK_SIZE)]

for i, block in enumerate(blocks, start=1):
    prompt = "\n".join([f"{m['role'].upper()} : {m['content']}" for m in block])
    user_content = f"Voici un extrait de conversation.\n\n{prompt}\n\nFais un résumé clair, concis et utile de cet échange pour usage mémoire IA."

    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un assistant spécialisé dans le résumé hiérarchique de conversations textuelles pour la mémoire longue d'une IA."},
            {"role": "user", "content": user_content}
        ]
    )

    summary = completion.choices[0].message.content

    db.collection("conversation_summaries").add({
        "user_id": USER_ID,
        "chunk_index": i,
        "summary": summary,
        "timestamp": datetime.utcnow()
    })

    logging.info(f"[HIERARCHY] Résumé du bloc {i} enregistré pour {USER_ID}")
