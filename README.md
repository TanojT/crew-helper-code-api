# 🧠 CrewCode Assistant

**CrewCode Assistant** is an enterprise-grade backend service that leverages LLMs and agentic workflows to assist developers with context-aware code generation, code updates, and modular task planning. It supports both open-source (LLaMA via Ollama) and proprietary (OpenAI GPT-4) models, orchestrated via a FastAPI application with CrewAI for dynamic agent execution.

---

## 🏗️ Overview

CrewCode Assistant helps enterprises enhance developer productivity by automating boilerplate generation, refactoring, and best-practice enforcement through intelligent agents. The system is built to support:

- **Stateless code generation**
- **Diff-based intelligent updates**
- **Model flexibility (GPT or LLaMA)**
- **Session-based project context handling**
- **Agentic pipelines using CrewAI**

---

## ✅ What’s Implemented

### 🚀 Core Features

| Feature                         | Description                                                                  |
| ------------------------------- | ---------------------------------------------------------------------------- |
| **Code Generation (Stateless)** | Accepts user input and returns language-specific, modular code               |
| **Diff Mode**                   | Updates existing code with new requirements using project-aware context      |
| **CrewAI Orchestration**        | Dynamic role-based agents (Planner, Writer, Updater) handle multi-step flows |
| **Session Context Management**  | Stores per-user/project file states (e.g., existing code, diffs) in memory   |
| **Multi-Model LLM Support**     | Supports OpenAI GPT-4 and Ollama-hosted LLaMA 3.2 models                     |
| **Markdown Output Formatting**  | Returns clean markdown code blocks, ready for frontend/editor consumption    |

---

## 🛠️ Architecture

```
User → FastAPI REST API
       ├─ Detects Mode (stateless / diff)
       ├─ Pulls context from SessionManager
       ├─ Builds prompt dynamically
       ├─ Invokes CrewAI with agents + tasks
       └─ Returns formatted code output
```

---

## 📁 Directory Structure

```
├── main.py                 # FastAPI app & endpoints
├── agents.py               # CrewAI agent definitions
├── llm_client.py           # LLM wrappers (OpenAI / Ollama)
├── session.py              # In-memory session manager
├── utils.py                # Helper functions (mode detection, markdown)
├── logger.py               # Structured logging
├── .env                    # API keys and config (ignored)
├── .gitignore              # Ignores venv, .env, pycache
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 🔐 Security & Privacy

- No user data or code is persisted beyond in-memory sessions
- Model API keys are stored securely via `.env` and never exposed in logs
- Future: Integrate with AWS Secrets Manager / Vault for secure key rotation

---

## 🧪 How to Run (Local Dev)

```bash
# Setup environment
python -m venv venv
source venv/bin/activate          # Or venv\Scripts\activate for Windows
pip install -r requirements.txt

# Add .env file
echo OPENAI_API_KEY=sk-... > .env

# Start FastAPI server
uvicorn main:app --reload
```

---

## 🧩 Future Roadmap

| Milestone | Description                                           |
| --------- | ----------------------------------------------------- |
| **C3**    | TTL-based session cleanup                             |
| **D**     | Agent expansion (CodeReviewer, Optimizer)             |
| **E**     | Vector database integration (for long context / RAG)  |
| **F**     | Editor integration (VSCode extension or web frontend) |
| **G**     | Authentication and multi-tenant project tracking      |

---

## 🧠 Vision

CrewCode Assistant is designed to evolve into a **developer co-pilot backend**, supporting IDE integrations, multi-user project memory, and enterprise-scale prompt management pipelines — without sacrificing model flexibility or deployment control.

---
