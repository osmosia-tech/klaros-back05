from flask import Blueprint, request, jsonify
from openai import OpenAI
from load_summary_history import load_summary_history
from load_hierarchy_summary import load_hierarchy_summary
from logger import log_and_vectorize
from memory_utils import load_conversation_history
from embedding_utils import get_embedding
from pinecone import Pinecone
import os
import logging
logging.basicConfig(level=logging.INFO)

# Initialisations
retriever_chatgpt3_bp = Blueprint("retriever_chatgpt3_bp", __name__)
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("klaros")

# Route principale de l'agent conversationnel avec mémoire
@retriever_chatgpt3_bp.route("/", methods=["POST"])
def chat_with_memory():
    data = request.json
    question = data.get("question")
    user_id = data.get("user_id", "elias_klaros")  # Valeur par défaut

    if not question:
        return jsonify({"error": "Missing 'question' field."}), 400

    # Charger l’historique Firestore
    history = load_conversation_history(user_id)
    logging.info(f"[MEMORY] {len(history)} messages récupérés pour {user_id}")

    # Charger les résumés compressés
    from load_summary_history import load_summary_history
    summaries = load_summary_history(user_id)
    logging.info(f"[SUMMARY] {len(summaries)} blocs de résumé chargés")

    # Créer le prompt complet pour GPT avec mémoire
    SYSTEM_PROMPT = "Tu es la mémoire longue de l’utilisateur. Tu as accès à son historique avec des messages datés."

    history = load_conversation_history(user_id)
    summaries = load_summary_history(user_id)
    hierarchy = load_hierarchy_summary(user_id)

    logging.info(f"[MEMORY] {len(history)} messages récupérés pour {user_id}")
    logging.info(f"[SUMMARY] {len(summaries)} blocs de résumé chargés")
    logging.info(f"[HIERARCHY] {len(hierarchy)} blocs hiérarchiques chargés")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += hierarchy
    messages += summaries
    messages += history
    messages += [{"role": "user", "content": question}]

# 3. DEBUG : afficher ce que GPT va recevoir
    print("📤 CONTENU ENVOYÉ À GPT :")
    for i, m in enumerate(messages):
        preview = m['content'][:200].replace('\n', ' ')
        print(f"[{i}] {m['role'].upper()} : {preview}{'...' if len(m['content']) > 200 else ''}")

    # Log de debug pour visualiser ce que reçoit GPT
    import json
    logging.info("======== CONTENU COMPLET DU PROMPT GPT ========")
    for idx, message in enumerate(messages):
        log_msg = f"[{idx}] {json.dumps(message, ensure_ascii=False)}"
        logging.info(log_msg)

    logging.info("======== CONTENU DU PROMPT GPT ========")
    for m in messages:
        logging.info(m)

    # Appel à GPT avec mémoire
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content

    # Logger et vectoriser la question
    log_and_vectorize(
        user_id=user_id,
        question=question,
        response=reply
    )

    return jsonify({
        "question": question,
        "context_used": "Mémoire Firestore chargée",
        "response": reply
    })
