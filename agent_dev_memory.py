import os
import logging
from datetime import datetime
from firebase_admin import firestore
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

# --- Initialisation Firestore et Pinecone ---
db = firestore.client()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("klaros")
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Fonction pour logger une évolution du code ---
def log_code_update(user_id, file, function, change_type, content):
    timestamp = datetime.utcnow().isoformat()
    doc_ref = db.collection("code_logs").document()

    log_data = {
        "user_id": user_id,
        "file": file,
        "function": function,
        "change_type": change_type,
        "content": content,
        "timestamp": timestamp
    }
    doc_ref.set(log_data)

    # Embedding
    embedding_input = f"{file}::{function}::{change_type}::{content}"
    embedding = openai.embeddings.create(
        model="text-embedding-3-small",
        input=embedding_input
    ).data[0].embedding

    vector_id = f"{user_id}-{timestamp}"
    index.upsert(vectors=[{
        "id": vector_id,
        "values": embedding,
        "metadata": {
            "user_id": user_id,
            "file": file,
            "function": function,
            "change_type": change_type,
            "text": content,
            "timestamp": timestamp
        }
    }])

    logging.info(f"[AGENT_DEV] Code log vectorisé → {vector_id}")


# --- Fonction pour charger les logs récents du code ---
def load_dev_history(user_id, limit=10):
    docs = db.collection("code_logs")\
        .where("user_id", "==", user_id)\
        .order_by("timestamp", direction=firestore.Query.DESCENDING)\
        .limit(limit).stream()

    messages = []
    for doc in docs:
        data = doc.to_dict()
        summary = f"[{data['file']} > {data['function']}] {data['change_type']} → {data['content']}"
        messages.append({
            "role": "system",
            "content": f"{summary}"
        })

    logging.info(f"[AGENT_DEV] {len(messages)} logs chargés pour {user_id}")
    return messages
