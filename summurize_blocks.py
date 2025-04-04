import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initialisation Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# Init OpenAI + Firestore
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
db = firestore.client()

# Fonction pour découper une liste en chunks
def chunk_messages(messages, size):
    return [messages[i:i + size] for i in range(0, len(messages), size)]

# Fonction pour résumer un bloc de messages
def summarize_block(messages):
    full_text = "\n\n".join([f"{m['role']}: {m['content']}" for m in messages])

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Tu vas recevoir un bloc de conversation entre un utilisateur et une IA. Résume les éléments clés, les sujets abordés et les intentions exprimées. Sois concis, clair, et structuré."
            },
            {
                "role": "user",
                "content": f"Voici le bloc de messages :\n\n{full_text}"
            }
        ]
    )

    return response.choices[0].message.content

# Fonction principale
def process_user_conversations(user_id, chunk_size=10):
    docs = (
        db.collection("conversations")
        .where("user_id", "==", user_id)
        .order_by("timestamp")
        .get()
    )

    messages = []
    for doc in docs:
        data = doc.to_dict()
        if data.get("question"):
            messages.append({"role": "user", "content": data["question"]})
        if data.get("response"):
            messages.append({"role": "assistant", "content": data["response"]})

    logging.info(f"[SUMMARIZE] {len(messages)} messages récupérés pour {user_id}")

    chunks = chunk_messages(messages, chunk_size)
    for i, chunk in enumerate(chunks):
        summary = summarize_block(chunk)
        doc_id = f"{user_id}_summary_{i+1}"
        db.collection("conversation_summaries").document(doc_id).set({
            "user_id": user_id,
            "summary": summary,
            "chunk_index": i+1,
            "timestamp": datetime.utcnow()
        })
        logging.info(f"[SUMMARY SAVED] Bloc {i+1} enregistré pour {user_id}")

# Exemple d'appel
if __name__ == "__main__":
    process_user_conversations(user_id="elias_klaros", chunk_size=10)
