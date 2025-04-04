from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("klaros")

stats = index.describe_index_stats()

print("Vecteurs par namespace :")
for ns in stats["namespaces"]:
    print(f"\nNamespace : {ns}")
    results = index.query(
        vector=[0.0]*1536,
        top_k=5,
        namespace=ns,
        include_metadata=True
    )
    for match in results["matches"]:
        print(f"- ID: {match['id']}, Text: {match['metadata'].get('text')}")
