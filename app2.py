# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore


# Initialiser Firebase
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

# Création de l'app Flask
app = Flask(__name__)
CORS(app)

# Import des différents blueprints
from shopify_routes import shopify_bp
from openai_routes import openai_bp
from advanced_routes import advanced_bp
from dev_agent import dev_agent_bp
from upsert_route import upsert_bp
from retriever_chatgpt3 import retriever_chatgpt3_bp


# Enregistrement des blueprints sur des préfixes
app.register_blueprint(shopify_bp, url_prefix="/shopify")
app.register_blueprint(openai_bp, url_prefix="/openai")
app.register_blueprint(advanced_bp, url_prefix="/advanced")
app.register_blueprint(dev_agent_bp, url_prefix="/dev")
app.register_blueprint(upsert_bp, url_prefix="/upsert")
app.register_blueprint(retriever_chatgpt3_bp, url_prefix="/chat")


print("✅ /chat route enregistrée")



# Test principal API
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "L'API fonctionne !"})

@app.route("/test-firestore", methods=["GET"])
def test_firestore():
    db = firestore.client()
    try:
        test_ref = db.collection("test").document("connexion")
        test_ref.set({"status": "success"})
        return jsonify({"success": True, "message": "Connexion Firestore réussie !"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

print(app.url_map)


if __name__ == "__main__":
    # Lancement Flask dev
    app.run(host="::", port=5084, debug=True)

