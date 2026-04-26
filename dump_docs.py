import os

docs = {
    "AGENTS.md": """# AGENTS.md — HELIX Master Agent Guide
## 3. Development Phases (Build In This Order)
### Phase 2 — Ingest (the data pipeline)
| Task | File | Depends On |
|------|------|------------|
| T-08 FileWatcher | helix/ingest/watcher.py | T-06 |
| T-09 FileRouter | helix/ingest/router.py | T-06 |
| T-10 IngestionQueue | helix/ingest/queue.py | T-06, T-09 |
| T-11 BaseProcessor | helix/ingest/processors/base.py | T-05 |
| T-12 ImageProcessor | helix/ingest/processors/image.py | T-11 |
| T-13 PDFProcessor | helix/ingest/processors/pdf.py | T-11 |
| T-14 TextProcessor | helix/ingest/processors/text.py | T-11 |
| T-15 DocumentProcessor | helix/ingest/processors/document.py | T-11 |
| T-16 VideoProcessor | helix/ingest/processors/video.py | T-11 |
| T-17 AudioProcessor | helix/ingest/processors/audio.py | T-11 |
| T-18 ChromaDB wrapper | helix/db/vector_store.py | T-05 |
### Phase 3 — Knowledge Layer
| T-19 WikiAgent | helix/agents/wiki_agent.py | T-11, T-06 |
| T-20 GraphBuilder | helix/agents/graph_builder.py | T-18, T-06 |
| T-21 QueryEngine | helix/agents/chat_engine.py (query methods) | T-18, T-19 |
| T-22 REST: files+search | helix/api/routes/files.py | T-07, T-21 |
### Phase 4 — Intelligence
| T-23 MemoryManager | helix/agents/memory_manager.py | T-05, T-06 |
| T-24 ChatEngine | helix/agents/chat_engine.py | T-21, T-23 |
| T-25 TaskAgent | helix/agents/task_agent.py | T-05, T-06, T-24 |
| T-26 CalendarAgent | helix/agents/calendar_agent.py | T-25 |
| T-27 ReflexAgent | helix/agents/reflex_agent.py | T-23, T-24 |
| T-28 Scheduler | helix/scheduler.py | T-25, T-26, T-27 |
### Phase 5 — Frontend
| T-29 Svelte scaffold | frontend/ | T-07 (API must be running) |
| T-30 Chat view | frontend/src/views/Chat.svelte | T-24, T-29 |
| T-31 Today view | frontend/src/views/Today.svelte | T-25, T-29 |
| T-32 Graph view | frontend/src/views/Graph.svelte | T-20, T-29 |
| T-33 Calendar view | frontend/src/views/Calendar.svelte | T-26, T-29 |
| T-34 Files + Tasks | frontend/src/views/Files.svelte | T-22, T-29 |
| T-35 Wiki view | frontend/src/views/Wiki.svelte | T-19, T-29 |
| T-36 Settings | frontend/src/views/Settings.svelte | T-29 |
### Phase 6 — Voice, Export, Polish
| T-37 VoiceGate | helix/voice/voice_gate.py | T-24 |
| T-38 TTS (optional) | helix/voice/tts.py | T-37 |
| T-39 ExportAgent | helix/agents/export_agent.py | T-05 |
| T-40 Notifications | helix/agents/task_agent.py (extension) | T-25 |
| T-41 Full REST API | helix/api/routes/api.py | All agents |
| T-42 Email processor | helix/ingest/processors/email_proc.py | T-11 |
| T-43 Test suite | tests/ | All phases |
| T-44 Install script | install.sh | All phases |
""",
    "ARCHITECTURE.md": "ARCHITECTURE",
    "DATABASE.md": "DATABASE",
    "SECURITY.md": "SECURITY",
    "TESTING_GUIDE.md": "TESTING_GUIDE",
}

for name, content in docs.items():
    with open(f"/app/{name}", "w") as f:
        f.write(content)
