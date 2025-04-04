# upsert_embeddings_only.py

from pinecone import Pinecone
from embedding_utils import get_embedding  # ta fonction d'embedding

# Supposons que l'index "klaros" est déjà créé à 1536 dimensions.
# On va juste se connecter et faire des upsert

# 1. Connecter Pinecone (version 6.x)
pc = Pinecone(
    api_key="pcsk_ppmy6_6nhKrKh24AyY9uh1SW7yU7c7sL2x1SBzh3npaLkMB9RcWhJJQsudR2e75yYLKm2",
    environment="us-east-1"
)

# 2. Récupérer l'index existant "klaros"
index = pc.Index("klaros")

# 3. Préparer tes documents
documents = [
    {
        "id": "docA",
        "text": "Nouveaux chiffres de ventes : 30 000€ de CA",
        "metadata": {"type": "rapport", "date": "2025-04-15"}
    },
    {
        "id": "docB",
        "text": "Campagne Google Ads : CPC=0.85€, CTR=3.0%, budget=4000€",
        "metadata": {"type": "ad_campaign", "platform": "Google"}
    }
]

# 4. Générer et upsert
vectors = []
for doc in documents:
    emb = get_embedding(doc["text"])  # => vecteur 1536
    vectors.append({
        "id": doc["id"],
        "values": emb,
        "metadata": {
            **doc["metadata"],
            "text": doc["text"]
        }
    })

index.upsert(
    vectors=vectors,
    namespace="client1"
)

print("Upsert terminé (embeddings uniquement) !")

# 5. (Optionnel) Faire une query pour valider
test_query = "Quels sont les nouveaux chiffres de ventes ?"
test_emb = get_embedding(test_query)
resp = index.query(
    vector=test_emb,
    top_k=2,
    namespace="client1",
    include_values=True,
    include_metadata=True
)
print("Query response :")
print(resp)
