from firebase_admin import firestore
from datetime import datetime
from embedding_utils import get_embedding
from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()

# Initialiser Pinecone une seule fois
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("klaros")  # Remplace par ton nom exact d'index

def log_and_vectorize(user_id, question, response):
    db = firestore.client()
    timestamp = datetime.utcnow().isoformat()

    # --- 1. Enregistrement dans Firestore ---
    doc = {
        "user_id": user_id,
        "question": question,
        "response": response,
        "timestamp": timestamp
    }
    db.collection("conversations").add(doc)

    # --- 2. Création de l'embedding depuis la question ---
    embedding = get_embedding(question)

    # --- 3. Enregistrement dans Pinecone ---
    vector = {
        "id": f"{user_id}-{timestamp}",
        "values": embedding,
        "metadata": {
            "user_id": user_id,
            "text": question,
            "timestamp": timestamp
        }
    }

    index.upsert(vectors=[vector], namespace="default")
    print(f"[PINECONE] Vector ajouté pour {user_id} dans Pinecone avec ID : {vector['id']}")

    # --- (optionnel) Confirmation console ---
    print(f"[MEMORY] Firestore + Pinecone OK → {user_id} | {timestamp}")
