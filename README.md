# 📝 Markdown Note Taking App

A fast and secure **note-taking backend** built with **FastAPI**, **PostgreSQL**, and **Redis**.  
It supports organizing notes in nested folders, version history, and real-time caching.  

---

## 🚀 Features

- ✍️ **Markdown notes** with title, text, tags, and metadata  
- 📂 **Nested folders** (folders inside folders)  
- 🗂️ **Version history** for every note    
- ⚡ **Caching layer** using Redis for faster responses  
- 🛡️ **JWT authentication** for secure access  
- 🐳 **Dockerized setup** for easy deployment  
- 🧪 **Pytest test suite** with async support  

---

## 🏗️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – async Python web framework  
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for database models  
- [PostgreSQL](https://www.postgresql.org/) – relational database  
- [Redis](https://redis.io/) – in-memory cache  
- [Docker](https://www.docker.com/) – containerized services  
- [Pytest](https://docs.pytest.org/) – testing framework  

---

## 📂 Project Structure

```
markdown-notes/
├── alembic/
│   ├── env.py
│   ├── versions/
├── src/
│   ├── main.py
│   ├── auth/
│   ├── common/
│   |   ├── db/
│   |   ├── exceptions/
│   |   ├── utils/
│   ├── config/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── services/
│   └── schemas/
├── tests/
├── docker-compose.yml
├── requirements.txt
└── README.md
```
---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/Kareem-Masalma/Markdown-Note-Taking-Project.git
cd Markdown-Note-Taking-Project
```

### 2. Configure environment variables
Create a `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/notes
REDIS_URL=redis://redis:6379
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
```

### 3. Run with Docker
```
docker-compose up --build
```
API will be available at:  
👉 `http://localhost:8000`

Docs:  
👉 Swagger UI → `http://localhost:8000/docs`  
👉 ReDoc → `http://localhost:8000/redoc`

---

## 🧪 Running Tests

```bash
pytest -v
```

---

## 🔑 Authentication

- Register & login to get a **JWT token**  
- Pass token in `Authorization: Bearer <token>` header  
