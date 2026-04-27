# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Build & Packaging Script for Windows
$ErrorActionPreference = "Stop"

Write-Host "Starting HELIX build process..."

# Build frontend
Write-Host "Building Svelte frontend..."
cd frontend
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Error "npm is required to build frontend."
    Return
}
npm install
npm run build
cd ..

# Build backend executable with PyInstaller
Write-Host "Building PyInstaller executable..."
if (-not (Get-Command "poetry" -ErrorAction SilentlyContinue)) {
    # Try using the .venv if it exists
    if (Test-Path ".venv\Scripts\poetry.exe") {
        $env:Path = "$PWD\.venv\Scripts;$env:Path"
    } else {
        Write-Error "poetry is required to build backend."
        Return
    }
}
poetry install
poetry run pyinstaller --name "helix-os" --onefile --add-data "frontend/dist;frontend/dist" helix/main.py

Write-Host "Build complete! Executable is in the dist/ folder."
