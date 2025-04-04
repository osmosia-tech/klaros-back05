from firebase_admin import firestore

def load_summary_history(user_id, limit=3):
    db = firestore.client()

    docs = (
        db.collection("conversation_summaries")
        .where("user_id", "==", user_id)
        .get()
    )

    # Tri manuel des blocs par chunk_index
    docs = sorted(docs, key=lambda doc: doc.to_dict().get("chunk_index", 0))

    # On limite à `limit` blocs
    docs = docs[:limit]

    messages = []
    for doc in docs:
        data = doc.to_dict()
        messages.append({
            "role": "system",
            "content": f"[Résumé bloc {data.get('chunk_index', '?')}] {data.get('summary', '')}"
        })
    return messages


    summaries = []
    for doc in docs:
        data = doc.to_dict()
        summary_text = data.get("summary")
        if summary_text:
            summaries.append({
                "role": "system",
                "content": f"Résumé de l'historique (bloc {data.get('chunk_index')}): {summary_text}"
            })

    return summaries
