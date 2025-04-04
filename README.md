# Klaros AI Backend

Klaros est un backend d’intelligence artificielle conçu pour construire des agents IA puissants, mémoriels et adaptatifs, capables de raisonner, d’interagir et de s’améliorer au fil du temps. Il s’appuie sur une architecture modulaire combinant GPT-4, Firebase Firestore, Pinecone, et des outils de traitement avancés (vision, embeddings, logs, etc.).

> **Objectif final :** Klaros vise à devenir une infrastructure IA complète pour copiloter des projets complexes, alimenter des chatbots avec mémoire longue, automatiser des actions ou encore servir de base à un assistant SaaS intelligent.

---

## 🧠 Fonctionnalités Clés

- 🧵 **IA contextuelle & mémorielle** : historique conversationnel horodaté (Firestore) + contexte vectoriel (Pinecone)
- 🤖 **Agent IA propulsé par GPT-4o** avec prompt dynamique et chargement hiérarchique du passé
- 🔍 **Recherche vectorielle** dans les questions passées (embeddings Ada v2 via OpenAI)
- 📷 **Analyse d’images** via CLIP + scoring contextuel (vision transformer)
- 📊 **Enregistrement automatique** des interactions (questions, réponses, embeddings)
- ⏰ **Historique horodaté** prêt à être interrogé ("qu’avais-tu dit le 3 mars ?")
- ⚙️ **Système d’upsert** performant (vector store + mémoire Firestore)
- 🤹 **Extensible** : endpoints personnalisables, support multi-agents, compatibilité API

---

## 🌐 Architecture Technique

| Composant              | Techno associée                      |
|------------------------|----------------------------------------|
| LLM                   | GPT-4o via OpenAI SDK                  |
| Mémoire contextuelle | Firebase Firestore                     |
| Mémoire vectorielle  | Pinecone + embeddings OpenAI (Ada v2) |
| Vision / Analyse      | Transformers / CLIPModel (HuggingFace) |
| Backend               | Flask (routes REST + CORS)            |
| Communication         | HTTPX, gRPC                            |
| Embeddings utils      | Python, Torch, Transformers            |

---

## 🔄 Endpoints Disponibles

| Endpoint                     | Description                                      |
|------------------------------|--------------------------------------------------|
| `POST /chat/`               | Interaction avec l'agent IA mémoriel            |
| `POST /upsert/sync`         | Synchro Firestore + Pinecone                    |
| `POST /upsert/upsertDirect` | Insertion directe d'une QA + embedding          |
| `POST /advanced/analyze-image` | Analyse d'image (CLIP)                     |
| `POST /openai/chat`         | Requête brute vers GPT                         |
| `POST /dev/execute`         | Execution d’actions / code via agent dev        |

---

## 🚀 Démarrage Rapide

```bash
# 1. Cloner le repo
git clone https://github.com/osmosia-tech/klaros-back05.git
cd klaros-back05

# 2. Créer un .env à partir du fichier exemple
cp .env.example .env
# (pense à y ajouter ta clé OpenAI, Pinecone, Firebase...)

# 3. Installer les dépendances (via venv ou non)
pip install -r requirements.txt

# 4. Lancer le serveur Flask
python app2.py
```

---

## 🚫 Fichiers Sensibles à Exclure (déjà dans `.gitignore`)
- `.env`
- `firebase_key.json`
- `venv/`, `__pycache__/`, `*.zip`, `*.pem`, `source/`

---

## �� Prochaines étapes envisagées

- Interface front type ChatGPT (React/Next.js)
- Système multi-agents avec mémoires isolées
- Plug-in d’analyse automatique des performances pub (Meta Ads)
- API compatible Shopify/Stripe/Notion pour copiloter des apps
- Comptes utilisateurs & authentification Firebase

---

## 🌎 Contribuer

> Ce projet est en phase active de développement. Toutes les issues, suggestions, PR sont les bienvenues.

---

Made with ❤️ by Elias @ Osmosia Tech

