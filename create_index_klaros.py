import os
from pinecone import Pinecone, ServerlessSpec, IndexMetadataConfig

def main():
    api_key = os.environ["PINECONE_API_KEY"]
    env = os.environ["PINECONE_ENV"]

    pc = Pinecone(api_key=api_key, environment=env)
    print(f"[Setup] Pinecone instance créée avec env={env}")

    index_name = "klaros"
    dimension = 1536
    metric = "cosine"
    region = "us-east-1"

    # Supprimer si existe
    existing = pc.list_indexes().names()
    if index_name in existing:
        pc.delete_index(index_name)

    # On utilise IndexMetadataConfig
    meta_cfg = IndexMetadataConfig(indexed=["*"])   # ou ["genre"], etc.

    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric=metric,
        spec=ServerlessSpec(
            cloud="aws",
            region=region
        ),
        metadata_config=meta_cfg
    )
    print(f"[Setup] Nouvel index '{index_name}' créé (dim={dimension}, metric={metric}, region={region}).")
    print("[Setup] metadata_config=IndexMetadataConfig(indexed=[\"*\"]) => filtrage sur toutes les metadata.")

if __name__ == "__main__":
    main()
