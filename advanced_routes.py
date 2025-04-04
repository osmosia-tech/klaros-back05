# advanced_routes.py
from flask import Blueprint, request, jsonify
import requests
import datetime
import pandas as pd
from PIL import Image
from firebase_admin import firestore
import torch
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=True)

advanced_bp = Blueprint("advanced_bp", __name__)

db = firestore.client()
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=True)

@advanced_bp.route("/analyze-image", methods=["POST"])
def analyze_product_image():
    data = request.json
    image_url = data.get("image_url")
    candidate_texts = data.get("texts", ["a product", "a piece of clothing", "a shoe"])

    if not image_url:
        return jsonify({"error": "L'URL de l'image est requise"}), 400

    try:
        image = Image.open(requests.get(image_url, stream=True).raw)
        inputs = clip_processor(text=candidate_texts, images=image, return_tensors="pt", padding=True)
        outputs = clip_model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        top_index = probs.argmax().item()

        return jsonify({
            "prediction": candidate_texts[top_index],
            "probability": probs[0][top_index].item()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@advanced_bp.route("/generate-insights", methods=["GET"])
def generate_insights():
    try:
        conversations = db.collection("clients").stream()
        all_data = []

        for client in conversations:
            client_data = client.to_dict()
            for convo in client_data.get("conversations", []):
                all_data.append({
                    "client": client_data["name"],
                    "question": convo["question"],
                    "response": convo["response"]
                })

        df = pd.DataFrame(all_data)
        top_questions = df["question"].value_counts().head(5)
        suggestions = [f"- Ajoutez une réponse détaillée pour : {q}" for q in top_questions.index]

        return jsonify({"insights": suggestions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
