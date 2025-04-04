from firebase_admin import firestore

def load_conversation_history(user_id, limit=10):
    db = firestore.client()

    # 1. Récupérer tous les messages pour ce user_id
    all_docs = (
        db.collection("conversations")
        .where("user_id", "==", user_id)
        .get()
    )

    # 2. Trier localement par timestamp croissant
    sorted_docs = sorted(
        all_docs,
        key=lambda doc: doc.to_dict().get("timestamp", ""),
        reverse=False
    )

    # 3. Ne garder que les derniers 'limit' messages
    limited_docs = sorted_docs[-limit:]

    # 4. Formater pour GPT
    history = []
    for doc in limited_docs:
        data = doc.to_dict()
        question = data.get("question")
        response = data.get("response")

        if question:
            history.append({"role": "user", "content": question})
        if response:
            history.append({"role": "assistant", "content": response})

    return history
