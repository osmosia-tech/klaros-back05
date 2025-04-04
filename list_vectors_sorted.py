from pinecone import Pinecone
from dotenv import load_dotenv
from datetime import datetime
import os

# Charger les variables d'environnement
load_dotenv()

# Initialiser Pinecone
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone_client.Index("klaros")  # Remplace si ton index s'appelle autrement

# Récupérer les stats de tous les namespaces
index_stats = index.describe_index_stats()

print("=== Vecteurs triés par timestamp ===\n")

all_matches = []

for namespace_name in index_stats["namespaces"]:
    results = index.query(
        vector=[0.0] * 1536,
        top_k=100,
        namespace=namespace_name,
        include_metadata=True
    )
    for match in results["matches"]:
        timestamp = match["metadata"].get("timestamp", "1970-01-01T00:00:00")
        try:
            ts_obj = datetime.fromisoformat(timestamp)
            ts_human_readable = ts_obj.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            ts_human_readable = "[timestamp inconnu]"

        all_matches.append({
            "id": match["id"],
            "text": match["metadata"].get("text", "[no text]"),
            "timestamp": timestamp,
            "timestamp_human": ts_human_readable,
            "namespace": namespace_name
        })

# Tri par timestamp ISO croissant
sorted_matches = sorted(all_matches, key=lambda x: x["timestamp"])

# Affichage formaté
for match in sorted_matches:
    print(f"[{match['timestamp_human']}] ({match['namespace']}) {match['id']} → {match['text']}")

