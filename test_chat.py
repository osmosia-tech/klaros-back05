import requests

url = "http://localhost:5000/chat"
data = {
    "user_id": "elias123",
    "message": "Quels sont les meilleurs produits à vendre en dropshipping en 2025 ?"
}

response = requests.post(url, json=data)
print("Réponse de l'IA :", response.json())

