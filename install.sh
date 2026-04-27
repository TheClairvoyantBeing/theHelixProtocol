#!/bin/bash
# HELIX Install Script
# Copyright (c) 2026 HELIX. All rights reserved.

echo "Installing HELIX dependencies using Poetry..."
poetry install || true

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Creating executable..."
poetry run pyinstaller --onefile --name helix --clean \
    --add-data "frontend/dist:frontend/dist" \
    --hidden-import="aiosqlite" \
    --hidden-import="uvicorn" \
    --hidden-import="fastapi" \
    --hidden-import="sqlalchemy" \
    --hidden-import="chromadb" \
    helix/main.py || true

echo "Build complete! Executable is located in the dist/ folder."
