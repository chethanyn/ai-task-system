🚀 AI Task System

This project is a full-stack application built using FastAPI (Backend) and React (Frontend) with AI-powered semantic search.

---

📌 Project Overview

The AI Task System allows users to:

- Register/Login using JWT authentication
- Manage tasks (create, update, view)
- Upload documents
- Perform AI-based semantic search on documents
- View analytics of tasks, users, and documents

---

🧠 Why This Project?

This project demonstrates:

- Full-stack development skills
- REST API design using FastAPI
- Authentication & authorization (JWT)
- Database management using SQLAlchemy
- AI integration using embeddings (MiniLM)
- Vector search using FAISS
- Frontend-backend integration

---

⚙️ Tech Stack

Backend

- FastAPI
- SQLAlchemy
- JWT Authentication
- FAISS (Vector Search)
- Sentence Transformers (MiniLM)

Frontend

- React (Vite)
- Axios

---

🔐 Features

1. Authentication

- User login with JWT token
- Secure API access

2. Task Management

- Create tasks
- View tasks
- Update task status (pending/completed)

3. Document Upload

- Upload text documents
- Store in database
- Convert to embeddings

4. AI Semantic Search

- Search documents using natural language
- Uses embeddings + FAISS for similarity search

5. Analytics

- Total tasks
- Completed tasks
- Pending tasks
- Total users
- Total documents

---

📂 Project Structure

AI-Task-System/
│
├── backend/
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── utils/
│   ├── main.py
│
├── frontend/
│   ├── src/
│   ├── App.jsx
│
└── README.md

---

▶️ How to Run

Backend

cd backend
uvicorn main:app --reload

---

Frontend

cd frontend
npm install
npm run dev

---

🌐 API Endpoints

- "/auth/login" → Login
- "/tasks/" → Task management
- "/documents/" → Upload documents
- "/search/" → AI search
- "/analytics/" → Project analytics

---

🎯 Conclusion

This project successfully combines backend development, frontend integration, and AI capabilities to build a complete real-world system.

