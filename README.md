# 🧠 SHL Conversational Assessment Recommender

An intelligent, conversational API that helps hiring managers find relevant SHL assessments through natural language dialogue. Built with **FastAPI, TF-IDF vector search, and rule-based agent logic**.

---

## 🚀 Live Demo

🔗 **[https://shl-ai-agent-vmre.onrender.com/](https://shl-ai-agent-vmre.onrender.com/)**

| Endpoint | URL |
|----------|-----|
| 🏠 **Root** | https://shl-ai-agent-vmre.onrender.com/ |
| 💚 **Health** | https://shl-ai-agent-vmre.onrender.com/health |
| 📚 **API Docs** | https://shl-ai-agent-vmre.onrender.com/docs |

---

## 📌 Features

| Feature | Description |
|---------|-------------|
| 💬 **Clarification** | Asks for missing info (seniority, skills, role) when query is vague |
| 📊 **Recommendations** | Returns 1-10 relevant SHL assessments with names, URLs, and test types |
| 🔄 **Refinement** | Updates recommendations when user constraints change mid-conversation |
| ⚖️ **Comparison** | Handles "difference between X and Y" queries using catalog evidence |
| 🚫 **Refusal** | Politely rejects out-of-scope questions (legal, hiring advice, prompt injection) |
| 🔍 **Semantic Search** | TF-IDF vectorization + cosine similarity over 377 SHL assessments |
| 📁 **Stateless API** | Every request carries full conversation history (no server-side state) |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Core programming language |
| **FastAPI** | RESTful API framework |
| **Uvicorn** | ASGI server for FastAPI |
| **scikit-learn** | TF-IDF vectorization & cosine similarity |
| **Pandas** | Data manipulation for catalog processing |
| **NumPy** | Numerical operations for search indexing |
| **Render.com** | Cloud deployment (Free Tier) |

---

## 📂 Project Structure
