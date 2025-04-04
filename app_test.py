from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/chat/", methods=["POST"])
def test_chat():
    print("🔥 ROUTE TRIGGÉE")
    return jsonify({"response": "Route test OK ✅"})

if __name__ == "__main__":
    print("�� Lancement app_test.py")
    app.run(debug=True, port=5050)
