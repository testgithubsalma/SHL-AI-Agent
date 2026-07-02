# 🧠 SHL Conversational Assessment Recommender

A stateless FastAPI service that helps hiring managers find relevant SHL assessments through natural language conversation. The agent clarifies vague queries, recommends 1-10 assessments, handles refinements, compares products, and refuses out-of-scope questions.

## 🚀 Live Demo

- **Base URL**: https://shl-ai-agent-vmre.onrender.com
- **Health Check**: https://shl-ai-agent-vmre.onrender.com/health
- **API Docs**: https://shl-ai-agent-vmre.onrender.com/docs

---

## 📋 Features

| Feature | Description |
|---------|-------------|
| 🔍 **Semantic Search** | TF-IDF vectorization + cosine similarity over 377 SHL assessments |
| 💬 **Clarification** | Asks for missing info (seniority, skills, role) when query is vague |
| 📊 **Recommendations** | Returns 1-10 relevant assessments with names, URLs, and test types |
| 🔄 **Refinement** | Updates recommendations when user constraints change mid-conversation |
| ⚖️ **Comparison** | Handles "difference between X and Y" queries using catalog evidence |
| 🚫 **Refusal** | Politely rejects out-of-scope questions (legal, hiring advice, prompt injection) |

---

## 🏗️ Architecture
