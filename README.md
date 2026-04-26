# HELIX Personal Intelligence OS

HELIX is a fully local, GPU-accelerated Personal Intelligence Operating System. It runs entirely on your machine, never sending data to external servers. It ingests your files, understands content deeply using local LLMs, organizes knowledge into a graph, surfaces reminders and tasks, and provides a chat interface with persistent memory.

## Features
- **Local & Private:** Zero telemetry. All processing and inference happen locally using Ollama or LM Studio.
- **Multimodal Ingestion:** Understands text, PDFs, images (via vision models), video, and audio (via faster-whisper).
- **Three-Tier Memory System:** Working memory, episodic memory (conversation logs), and semantic memory (knowledge graph and rules).
- **Self-Improving (Reflexion):** HELIX analyzes past conversations to extract behavioral rules and user preferences to improve future responses.
- **Knowledge Graph:** Automatically links concepts, people, and projects.
- **Modular Agents:** Features distinct agents for Chat, Wiki, Tasks, Calendar, Memory, and System reflection.
- **Encrypted Exports:** Export sensitive data securely using AES-256-GCM encryption.

## Prerequisites

To run HELIX from source, you will need:
- **Python 3.11+**
- **Node.js 20+**
- **Poetry 1.8+** (for Python dependency management)
- **Ollama** installed and running on your machine
- **ffmpeg** and **Tesseract OCR** (installed and added to your system PATH)
- *(Optional but Recommended)* NVIDIA GPU with CUDA 12.1+ drivers for hardware acceleration.

## First-Time Setup

1. **Clone the repository and install backend dependencies:**
   ```bash
   git clone https://github.com/yourusername/helix.git
   cd helix
   poetry install
   ```

2. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Start the Application:**
   Start the Python backend server:
   ```bash
   poetry run python -m helix.main --dev &
   ```
   Start the Svelte frontend development server:
   ```bash
   cd frontend
   npm run dev &
   ```

## Usage

1. Open your web browser to `http://localhost:5173` (or the port specified by Vite in the frontend terminal). The backend API runs on `http://localhost:7331`.
2. Configure your Vault directories (e.g., `~/Documents`, `~/Pictures`) by modifying `~/.helix/config.toml` or using the UI Settings.
3. HELIX will automatically begin indexing and processing files found in the configured directories.
4. Use the Chat interface to ask questions about your files. HELIX will reference your documents and remember past context.

## Documentation
For more detailed information on the architecture, testing, and security policies, please read the provided `.md` documentation files in the repository root.
