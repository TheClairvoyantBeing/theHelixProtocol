# HELIX Virtual Environment Setup Script for Windows
# Copyright (c) 2026 HELIX. All rights reserved.

Write-Host "Setting up Python virtual environment..."
python.exe -m venv .venv
. .\.venv\Scripts\Activate.ps1

Write-Host "Installing poetry..."
pip install poetry

Write-Host "Installing dependencies..."
poetry install

Write-Host "Setting up frontend..."
cd frontend
npm install
cd ..

Write-Host "Environment setup complete."
