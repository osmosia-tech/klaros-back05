# shopify_routes.py
from flask import Blueprint, request, jsonify, redirect
import re
import secrets
import requests
from firebase_admin import firestore

shopify_bp = Blueprint("shopify_bp", __name__)

# Tes clés shopify (si tu veux, tu peux aussi les mettre en variable d'env)
SHOPIFY_API_KEY = "d3cee4ef071a69ec189fe0a316f2740a"
SHOPIFY_API_SECRET = "cac5fe4c9d6f19e3211b48adf7443fab"

db = firestore.client()

def get_token_for_shop(shop):
    doc = db.collection("shops").document(shop).get()
    if doc.exists:
        return doc.to_dict().get("access_token")
    return None

@shopify_bp.route("/auth")
def shopify_auth():
    shop = request.args.get("shop")
    if not shop or not re.match(r"^[a-zA-Z0-9\-]+\.myshopify\.com$", shop):
        return "Paramètre 'shop' invalide", 400

    redirect_uri = "http://3.104.110.5/shopify/callback"
    scopes = "read_products,read_orders"
    state = secrets.token_urlsafe(16)

    install_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={SHOPIFY_API_KEY}&scope={scopes}&redirect_uri={redirect_uri}&state={state}"
    )
    return redirect(install_url)

@shopify_bp.route("/callback")
def shopify_callback():
    shop = request.args.get("shop")
    code = request.args.get("code")

    if not shop or not code:
        return "Paramètres manquants", 400

    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": SHOPIFY_API_KEY,
        "client_secret": SHOPIFY_API_SECRET,
        "code": code
    }

    response = requests.post(token_url, json=payload)
    if response.status_code != 200:
        return f"Erreur de token : {response.text}", 400

    data = response.json()
    access_token = data.get("access_token")

    db.collection("shops").document(shop).set({
        "access_token": access_token,
        "installed_at": firestore.SERVER_TIMESTAMP,
        "shop": shop
    })

    return "App installée avec succès sur la boutique Shopify !"

@shopify_bp.route("/<shop>/products", methods=["GET"])
def get_shopify_products(shop):
    token = get_token_for_shop(shop)
    if not token:
        return jsonify({"error": "Token introuvable"}), 403

    url = f"https://{shop}/admin/api/2024-01/products.json"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()["products"])
    return jsonify({"error": "Erreur Shopify"}), response.status_code

@shopify_bp.route("/<shop>/order/<order_id>", methods=["GET"])
def get_shopify_order(shop, order_id):
    token = get_token_for_shop(shop)
    if not token:
        return jsonify({"error": "Token introuvable"}), 403

    url = f"https://{shop}/admin/api/2024-01/orders.json?name={order_id}"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.json().get("orders"):
        return jsonify(response.json()["orders"][0])
    return jsonify({"error": "Commande introuvable"}), 404

@shopify_bp.route("/<shop>/me", methods=["GET"])
def get_shop_info(shop):
    token = get_token_for_shop(shop)
    if not token:
        return jsonify({"error": "Token introuvable"}), 403

    url = f"https://{shop}/admin/api/2024-01/shop.json"
    headers = {"X-Shopify-Access-Token": token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()["shop"])
    return jsonify({"error": "Erreur Shopify"}), response.status_code
