import firebase_admin
from firebase_admin import credentials, firestore
from pinecone import Pinecone  # version 6.x
from embedding_utils import get_embedding  # ta fonction, qui appelle openai.Embedding
import os
from dotenv import load_dotenv
load_dotenv()

firebase_key_path = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")

# Initialisation sécurisée de Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)

# Client Firestore
db = firestore.client()

# 1. Initialiser Pinecone
pc = Pinecone(
    api_key="pcsk_ppmy6_6nhKrKh24AyY9uh1SW7yU7c7sL2x1SBzh3npaLkMB9RcWhJJQsudR2e75yYLKm2",  # <-- Remplace par ta vraie clé
    environment="us-east-1"
)

index = pc.Index("klaros")  # suppose que l'index "klaros" (1536D) est déjà créé

########################################
# FONCTION 1: SYNC_CONVERSATIONS
########################################
def sync_conversations():
    """
    Récupère toutes les conversations (docs) de Firestore (collection "conversations"),
    génère l’embedding pour chacune, et upsert le tout dans Pinecone d’un coup.
    """
    docs = db.collection("conversations").get()
    
    vectors = []
    for doc_snap in docs:
        doc_data = doc_snap.to_dict()
        message_text = doc_data.get("message", "")
        
        # 1) Générer l'embedding
        emb = get_embedding(message_text)
        
        # 2) Préparer l'upsert
        vectors.append({
            "id": doc_snap.id,  # l'ID Firestore
            "values": emb,
            "metadata": {
                "text": message_text,
                "timestamp": doc_data.get("timestamp", ""),  # string par défaut
                "author": doc_data.get("author", "unknown")
                # autres champs éventuels
            }
        })
    
    # 3) Upsert en lot dans Pinecone (namespace "default" par exemple)
    if vectors:
        index.upsert(vectors=vectors, namespace="default")
        print(f"{len(vectors)} messages synchronisés vers Pinecone!")
    else:
        print("Aucun message à synchroniser.")

########################################
# FONCTION 2: ADD_CONVERSATION_DIRECT
########################################
def add_conversation_direct(message, author="user", timestamp=None):
    """
    Ajoute immédiatement un nouveau doc dans Firestore,
    génère l'embedding, et upsert dans Pinecone dans la foulée.
    """
    # Si on veut s'assurer que timestamp est toujours une string (sinon Pinecone plante sur None)
    if timestamp is None:
        timestamp = ""

    # 1) Créer le document Firestore dans "conversations"
    doc_ref = db.collection("conversations").document()  # ID auto
    doc_id = doc_ref.id

    data_doc = {"message": message, "author": author, "timestamp": timestamp}
    doc_ref.set(data_doc)

    # 2) Générer l'embedding
    emb = get_embedding(message)

    # 3) Upsert Pinecone
    vector = [{
        "id": doc_id,  # On utilise l'ID Firestore comme ID Pinecone
        "values": emb,
        "metadata": {
            "text": message,
            "author": author,
            "timestamp": timestamp
        }
    }]
    index.upsert(vectors=vector, namespace="default")

    print(f"Doc {doc_id} => Firestore + Pinecone (direct) insérés.")

########################################
# TEST / MAIN
########################################
if __name__ == "__main__":
    # EXEMPLE 1 : on fait un "batch" pour toutes les conversations existantes
    sync_conversations()

    # EXEMPLE 2 : on ajoute 1 nouveau message direct
    add_conversation_direct("Bonjour direct!", "assistant")
