import openai
import os
from dotenv import load_dotenv

# ✅ Charger les variables d’environnement
load_dotenv()

# ✅ Créer un client OpenAI avec la bonne clé
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        model=model,
        input=[text]
    )
    return response.data[0].embedding

if __name__ == "__main__":
    test_text = "Bonjour, ceci est un test d'embedding."
    emb = get_embedding(test_text)
    print("Dimension:", len(emb))
    print("Extrait du vecteur:", emb[:5])
