# theHelixProtocol 🧬

> **A local-first Personal Intelligence OS — index your files, chat with your data, and build a knowledge graph, all running privately on your machine.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-≥3.11-blue.svg)
![Svelte](https://img.shields.io/badge/Svelte-5-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)

HELIX watches your local directories, ingests files (PDFs, images, documents, audio, video), indexes them into a vector database, and lets you chat with a local LLM that has RAG-powered access to your personal data vault.

---

## ✨ Features

- **RAG-Powered Chat** — Ask questions about your files. HELIX retrieves relevant context from your vault and streams answers via a local LLM.
- **Multiformat Ingestion** — Processes PDFs, DOCX, XLSX, PPTX, images (with EXIF), audio, video, and plain text.
- **Knowledge Graph** — Automatically builds a node-edge graph linking files, concepts, and wiki pages. Interactive D3.js visualisation.
- **Tiered Hardware Detection** — Auto-selects the right Ollama model (from `llama3:70b` to `gemma:2b`) based on your GPU/VRAM.
- **Task & Calendar Management** — Track tasks, set deadlines, get reminders. Calendar view via FullCalendar.
- **Memory System** — Three-tier memory (working, episodic, semantic). HELIX learns your preferences over time.
- **Self-Improvement (Reflex Agent)** — Periodically analyses conversations to extract behavioural rules and improve responses.
- **Encrypted Exports** — AES-256-GCM encrypted backup archives of your vault data.
- **Local-First & Private** — Everything runs on your machine. No cloud, no telemetry, no data leaves your device.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn, SQLAlchemy 2.0 (async SQLite) |
| Vector DB | ChromaDB (persistent, local) |
| LLM | Ollama (local) — supports Llama 3, Mistral, Phi-3, Gemma |
| Frontend | Svelte 5, Vite, TailwindCSS 3, D3.js, FullCalendar |
| Encryption | `cryptography` (AES-256-GCM with PBKDF2) |

---

## 🚀 Prerequisites

1. **Python ≥ 3.11** — [python.org](https://www.python.org/downloads/)
2. **Poetry** — `pip install poetry`
3. **Ollama** — [ollama.com](https://ollama.com/) (must be running locally)
4. **Node.js ≥ 18** — [nodejs.org](https://nodejs.org/) (for the frontend)

Pull at least one model in Ollama:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/TheClairvoyantBeing/theHelixProtocol.git
cd theHelixProtocol

# Install Python dependencies
poetry install

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Configuration (Optional)

Create `~/.helix/config.toml` to customise vault directories:

```toml
[vault]
root_dirs = ["~/Documents", "~/Pictures", "~/Projects"]
debug = false

[model]
ollama_base = "http://localhost:11434"
# force_tier = 3  # Override auto-detection

[ui]
theme = "dark"
port = 7331
```

---

## ▶️ Running

```bash
# Terminal 1: Start the backend
poetry run python -m helix.main

# Terminal 2: Start the frontend dev server
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

For production, build the frontend and let FastAPI serve it:
```bash
cd frontend && npm run build && cd ..
poetry run python -m helix.main
# Open http://localhost:7331
```

---

## 🏗️ Architecture

```
helix/
├── main.py              # Orchestrator — starts all agents and FastAPI
├── config.py            # TOML configuration (Pydantic)
├── hardware.py          # GPU/CPU detection and tiering
├── model_selector.py    # Auto-selects Ollama models by hardware
├── llm_client.py        # Ollama API client (text, vision, embeddings)
├── event_bus.py         # Async pub/sub for agent communication
├── scheduler.py         # Nightly consolidation jobs
├── agents/
│   ├── chat_engine.py   # RAG chat with vector search
│   ├── memory_manager.py# 3-tier memory persistence
│   ├── wiki_agent.py    # Auto-generates markdown knowledge pages
│   ├── graph_builder.py # Builds SQLite knowledge graph
│   ├── task_agent.py    # Task lifecycle + reminders
│   ├── calendar_agent.py# Calendar event monitoring
│   ├── reflex_agent.py  # Self-improvement via LLM reflection
│   └── export_agent.py  # AES-256-GCM encrypted backups
├── api/                 # FastAPI routes + Pydantic schemas
├── db/                  # SQLAlchemy + ChromaDB + migrations
├── ingest/              # File watcher + processor pipeline
│   └── processors/      # PDF, image, audio, video, document, etc.
└── voice/               # Voice input/TTS (experimental)

frontend/                # Svelte 5 + Vite SPA
├── src/
│   ├── views/           # Chat, Files, Graph, Today, Calendar, Settings
│   ├── components/      # Ribbon, Sidebar
│   ├── stores/          # Svelte stores
│   └── lib/             # API client
```

---

## 🧪 Testing

```bash
poetry run pytest tests/ -v
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
