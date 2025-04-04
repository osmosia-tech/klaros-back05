# upsert_routes.py
from flask import Blueprint, request, jsonify
from firestone_bridge4 import sync_conversations, add_conversation_direct

upsert_bp = Blueprint("upsert_bp", __name__)

@upsert_bp.route("/sync", methods=["POST"])
def sync_endpoint():
    """
    Appelle la fonction sync_conversations() pour tout indexer en bloc.
    """
    sync_conversations()
    return jsonify({"message": "Synchronisation effectuée."})

@upsert_bp.route("/upsertDirect", methods=["POST"])
def upsert_direct_endpoint():
    """
    Appelle add_conversation_direct(...) pour ajouter un message 
    instantanément dans Firestore/Pinecone.
    Attendu un JSON : {"message": "...", "author": "...", "timestamp": "..."}
    """
    data = request.json
    msg = data.get("message", "")
    author = data.get("author", "user")
    ts = data.get("timestamp", "")

    add_conversation_direct(msg, author, ts)
    return jsonify({"message": "Message upsert direct OK."})
