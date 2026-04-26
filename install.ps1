# HELIX Install Script for Windows
# Copyright (c) 2026 HELIX. All rights reserved.

Write-Host "Installing HELIX dependencies using Poetry..."
poetry install

Write-Host "Building frontend..."
cd frontend
npm install
npm run build
cd ..

Write-Host "Creating executable..."
poetry run pyinstaller --onefile --name helix.exe --clean `
    --add-data "frontend/dist;frontend/dist" `
    helix/main.py

Write-Host "Build complete! Executable is located in the dist/ folder."
