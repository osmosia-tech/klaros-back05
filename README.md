# Klaros AI Backend

**Klaros** est un backend intelligent pour agents IA augmentés par la mémoire. Il combine OpenAI (GPT-4), Pinecone (mémoire vectorielle), Firebase Firestore (mémoire contextuelle), et de puissants outils ML (Transformers, Torch, etc.) pour créer un système d'IA conversationnelle évolutif et persistant.

---

## 🧠 Fonctionnalités

- 🔁 Mémoire longue via Firebase Firestore
- 🧠 Moteur vectoriel Pinecone avec embeddings OpenAI
- 🔌 Plug-ins IA compatibles Transformers, Torch & CUDA
- 🧩 Intégration GPT-4 via OpenAI SDK
- 💬 Upload JSON d’historiques de ChatGPT (pour continuité)
- 🧰 Conçu pour des agents IA multi-contexte et évolutifs

---

## 🔧 Stack Technique

| Composant           | Technologie utilisée                         |
|---------------------|-----------------------------------------------|
| Backend API         | Flask 3.1                                     |
| Mémoire Contextuelle| Firebase Firestore                            |
| Mémoire Vectorielle | Pinecone (client + plugins assistant/interface) |
| LLM                 | OpenAI GPT-4 (via SDK officiel)               |
| Embedding/ML        | HuggingFace, Transformers, Torch, Triton, CUDA |
| Données/Logs        | Pandas, NumPy, Loguru                         |
| Communication       | HTTPX, gRPC, Flask-CORS                       |
| Déploiement         | Gunicorn                                      |

---

## 🚀 Démarrage Rapide

### 1. Cloner le projet

```bash
git clone https://github.com/osmosia-tech/klaros-backend-live.git
cd klaros-backend-live

