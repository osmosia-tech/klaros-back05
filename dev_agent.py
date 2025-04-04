# dev_agent.py
from flask import Blueprint, request, jsonify
import subprocess

dev_agent_bp = Blueprint("dev_agent_bp", __name__)

@dev_agent_bp.route("/execute", methods=["POST"])
def dev_execute():
    data = request.json
    actions = data.get("actions", [])
    results = []

    for action in actions:
        # Gérer create_file, install_package, etc.
        ...
    return jsonify({"results": results})
