# 🧩 SmartBiz AI — Co-Pilot Agent Instructions.md

This document contains **complete technical instructions** for setting up, developing, and deploying the **SmartBiz AI Co-Pilot Agent** using best-practice stack architecture, VS Code configurations, and deployment workflows.

---

## ⚙️ 1. Tech Stack Overview

| Layer | Technology | Description |
|--------|-------------|-------------|
| Frontend | **React + Tailwind + TypeScript** | Web UI with chat and dashboard |
| Backend | **FastAPI (Python 3.10+)** | API orchestration + AI task routing |
| Database | **PostgreSQL (SQLAlchemy ORM)** | Stores business & user data |
| Authentication | **Firebase Auth / JWT** | User management and auth |
| AI Layer | **LangChain / LlamaIndex** | AI orchestration & reasoning |
| Memory Layer | **OpenMemory** | Private contextual memory for MSME data |
| Model Access | **Unified AI Gateway / OpenAI API** | Secure model integration |
| Task Queue | **Celery + Redis** | Background task management |
| Hosting | **Vercel (Frontend)** + **AWS/GCP (Backend)** | Scalable deployment |

---

## 🧱 2. Folder Structure

```
SmartBizAI/
│
├── frontend/                # React/Next.js UI
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/        # API calls to FastAPI backend
│   │   └── styles/
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── main.py              # Entry point
│   ├── api/                 # Route definitions
│   ├── core/                # Config, security, utils
│   ├── models/              # SQLAlchemy models
│   ├── services/            # Business logic modules
│   ├── orchestrator/        # AI task routing & management
│   ├── memory/              # OpenMemory integration
│   └── requirements.txt
│
├── scripts/                 # Automation or cron jobs
├── .vscode/                 # VS Code workspace configs
├── docker-compose.yml       # Container orchestration
├── Dockerfile               # Build backend container
├── .env                     # Environment variables
└── README.md
```

---

## 🧠 3. Best Practice Rules

1. Keep routes modular (1 file per domain)
2. Sanitize user inputs before sending to AI models
3. Store sensitive data securely in encrypted DB fields
4. Implement AI intent classification before workflow routing
5. Cache repetitive API calls with Redis/local cache
6. Maintain structured logs (use `logging` module)
7. Persist context with OpenMemory between sessions
8. Add retry logic for unstable API calls
9. Write unit tests using `pytest`
10. Use environment-based configuration (`dev`, `prod`)

---

## 🧩 4. FastAPI Co-Pilot Boilerplate

```python
from fastapi import FastAPI, Request
from openai import OpenAI
from openmemory import Memory

app = FastAPI(title="SmartBiz AI Co-Pilot")

client = OpenAI(api_key="YOUR_API_KEY")
memory = Memory(path="./memory_store")

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    query = data.get("query")

    context = memory.get_context(user_id)
    prompt = f"Context: {context}\nUser Query: {query}\nRespond as a helpful MSME co-pilot."

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    memory.update_context(user_id, query, answer)
    return {"reply": answer}
```

---

## 🧰 5. VS Code Setup

### 📄 `.vscode/tasks.json`
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run FastAPI Backend",
      "type": "shell",
      "command": "uvicorn backend.main:app --reload --port 8000",
      "group": {"kind": "build", "isDefault": true}
    },
    {
      "label": "Run React Frontend",
      "type": "shell",
      "command": "npm start --prefix frontend",
      "group": "build"
    },
    {
      "label": "Run Both (SmartBiz Fullstack)",
      "dependsOn": ["Run FastAPI Backend", "Run React Frontend"],
      "dependsOrder": "parallel"
    }
  ]
}
```

### 🧑‍💻 `.vscode/launch.json`
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug FastAPI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/main.py",
      "console": "integratedTerminal"
    },
    {
      "name": "Debug React Frontend",
      "type": "pwa-chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

### ⚙️ `.vscode/settings.json`
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "editor.formatOnSave": true,
  "editor.tabSize": 4,
  "eslint.validate": ["javascript", "typescript"],
  "prettier.singleQuote": true,
  "prettier.semi": false
}
```

### 💡 Recommended Extensions
- `ms-python.python`
- `ms-python.debugpy`
- `ms-vscode.js-debug`
- `dbaeumer.vscode-eslint`
- `esbenp.prettier-vscode`
- `humao.rest-client`
- `ms-azuretools.vscode-docker`
- `GitHub.copilot`

---

## 🐳 6. Docker Setup

### `Dockerfile`
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY backend/ ./backend
RUN pip install -r backend/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`
```yaml
version: '3.9'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
    command: npm start
    ports:
      - "3000:3000"

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: smartbiz
    ports:
      - "5432:5432"
```

---

## 🚀 7. Developer Setup Guide

1. **Install dependencies:**
   ```bash
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```
2. **Run both apps in VS Code:** Press `Ctrl+Shift+B` → choose *Run Both (SmartBiz Fullstack)*.
3. **Debug:** Press `F5` → select *Debug FastAPI* or *Debug React Frontend*.
4. **Docker Run:**
   ```bash
   docker-compose up --build
   ```

---

## 🔐 8. Security & Privacy Notes
- Encrypt stored MSME business data (AES256).
- Use OpenMemory for secure contextual data.
- Redact personal or financial info before sending to AI.
- Restrict API access by JWT or OAuth2.

---

## ☁️ 9. Deployment Steps
1. Push repo to GitHub.
2. Connect frontend to **Vercel** (auto-builds React).
3. Deploy backend to **AWS ECS / Render / Cloud Run**.
4. Set environment variables securely in deployment platform.

---

## 🧭 10. Vision
> “Empowering every Indian MSME with an AI co-pilot that simplifies operations, automates compliance, and accelerates growth — securely and intelligently.”

---

✅ **End of Co-Pilot Instructions.md**