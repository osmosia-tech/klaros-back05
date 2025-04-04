import openai
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Nouveau client compatible avec openai>=1.0.0
client = openai.OpenAI()

# Requête simple à GPT-3.5
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Tu es un assistant très utile."},
        {"role": "user", "content": "Est-ce que tu me comprends ?"}
    ]
)

# Afficher la réponse
print("Réponse de GPT-4o :", response.choices[0].message.content)



