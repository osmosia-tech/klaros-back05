# openai_routes.py
from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import datetime
import openai
from dotenv import load_dotenv
import os

# ✅ Chargement des variables d'environnement
load_dotenv()

# ✅ Initialisation Firebase (clé depuis firebase_key.json)
try:
    cred = credentials.Certificate("firebase_key.json")
    initialize_app(cred)
except ValueError:
    pass  # Firebase déjà initialisé

# ✅ Initialisation Firestore
db = firestore.client()

# ✅ Initialisation OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

# ✅ Création du Blueprint Flask
openai_bp = Blueprint("openai_bp", __name__)

def save_conversation(user_id, messages):
    db.collection("conversations").add({
        "user_id": user_id,
        "timestamp": datetime.datetime.now(),
        "messages": messages
    })

@openai_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    user_message = data.get("message")

    if not user_id or not user_message:
        return jsonify({"error": "user_id et message sont requis"}), 400

    try:
        print("✅ Appel GPT depuis /chat avec user_id:", user_id)

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es un assistant utile pour le e-commerce."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content

        save_conversation(user_id, [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": bot_reply}
        ])

        return jsonify({"response": bot_reply})

    except Exception as e:
        print("❌ Erreur OpenAI /chat:", str(e))
        return jsonify({"error": str(e)}), 500
