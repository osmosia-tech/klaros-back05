import os
import openai
from typing import List
from pinecone_setup import get_index, upsert_vectors

# Paramètres chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# On suppose OPENAI_API_KEY est défini via variables d'environnement
openai.api_key = os.environ.get("OPENAI_API_KEY")

def chunk_text(text: str, chunk_size:int=CHUNK_SIZE, overlap:int=CHUNK_OVERLAP) -> List[str]:
    """
    Découpe 'text' en segments ~chunk_size caractères,
    en glissant d'un 'chunk_size - overlap'.
    """
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def embed_text(chunk: str) -> List[float]:
    """
    Calcule l'embedding OpenAI (text-embedding-ada-002) pour un 'chunk'.
    """
    response = openai.Embedding.create(
        input=chunk,
        model="text-embedding-ada-002"
    )
    return response["data"][0]["embedding"]

def ingest_file(filepath:str, source:str="doc", namespace:str="klaros_data"):
    """
    Lit 'filepath', chunk, embed, upsert dans l'index existant.
    - source : label ("code", "chat", "doc"...) 
    - namespace : segmenter si besoin, ex. "klaros_data".
    """
    # Lire le fichier
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Chunk
    file_chunks = chunk_text(text)

    # Préparer la liste de vecteurs
    vectors = []
    for i, chunk in enumerate(file_chunks):
        emb = embed_text(chunk)
        doc_id = f"{os.path.basename(filepath)}_chunk{i}"
        meta = {
            "source": source,
            "filename": os.path.basename(filepath)
        }
        vectors.append({
            "id": doc_id,
            "values": emb,
            "metadata": meta
        })

    # Upsert via upsert_vectors (issu de pinecone_setup.py)
    upsert_vectors(vectors, namespace=namespace)

def main():
    # Exemple de fichiers à ingérer
    files_to_ingest = [
        "app.py",
        "dev_agent.py",
        # "mon_chat_history.txt",
    ]

    for fpath in files_to_ingest:
        # Déterminer le "source"
        if fpath.endswith(".py"):
            source = "code"
        elif "chat" in fpath:
            source = "chat"
        else:
            source = "doc"

        print(f"Ingesting {fpath} as {source} ...")
        ingest_file(filepath=fpath, source=source, namespace="klaros_data")

    print("Done ingestion.")

if _name_ == "_main_":
    main()
