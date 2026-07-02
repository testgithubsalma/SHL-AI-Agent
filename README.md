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
```text
shl-assessment-agent/

├── app/
├── scraper/
├── vector_db/
├── data/
├── prompts/
├── tests/
├── docs/

├── main.py
├── requirements.txt
├── README.md
└── .env
```

---

# 🛠️ Technologies Used

- 🐍 Python 3.11
- ⚡ FastAPI
- 🌐 Requests
- 🍜 BeautifulSoup
- 📊 Pandas
- 🧠 Sentence Transformers
- 🔎 FAISS
- 🤖 OpenAI / Gemini (Optional)
- ☁️ Render

---

# 🚀 API Endpoints

## ❤️ GET /health

Health check endpoint.

### Response

```json
{
  "status": "ok"
}
```

---

## 💬 POST /chat

Main conversational endpoint.

### Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need to hire a Java developer"
    }
  ]
}
```

---

### Response (Clarification)

```json
{
  "reply": "What is the seniority level? What specific skills are required?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

### Response (Recommendation)

```json
{
  "reply": "Based on your requirements, here are the recommended assessments.",
  "recommendations": [
    {
      "name": "Core Java (Advanced Level)",
      "url": "https://www.shl.com/...",
      "test_type": "Knowledge & Skills"
    }
  ],
  "end_of_conversation": false
}
```

---

# 🎯 Functionalities

The conversational agent supports the following behaviors:

- ✅ Clarifies vague hiring requests before recommending assessments
- ✅ Recommends between 1 and 10 SHL assessments
- ✅ Updates recommendations when user requirements change
- ✅ Compares SHL assessments using catalog information
- ✅ Rejects unrelated or out-of-scope requests
- ✅ Returns only assessments available in the SHL catalog

---

# 🧪 Evaluation

The project was evaluated using the provided public conversation traces.

### Tested Behaviors

- ✅ Clarification
- ✅ Recommendation
- ✅ Refinement
- ✅ Assessment Comparison
- ✅ Out-of-Scope Refusal
- ✅ End of Conversation Detection

---

# ☁️ Deployment

The application can be deployed on platforms such as **Render**.

### Required Endpoints

- `GET /health`
- `POST /chat`

---

# 🤖 AI Tools Used

The following AI tools were used during development:

- ChatGPT
- GitHub Copilot

These tools were used for brainstorming, debugging, implementation guidance, and documentation. The final implementation and integration were completed by the author.

---

# 👩‍💻 Author

**Salma**

Python | AI | Machine Learning Enthusiast

GitHub: **testgithubsalma**

---

# 📄 License

This project was developed solely for the **SHL AI Intern Take-Home Assignment** and is intended for evaluation purposes only.
