# Copyright (c) 2026 HELIX. All rights reserved.
# Helper script to set up Python & Node environment on Windows
$ErrorActionPreference = "Stop"

Write-Host "Setting up HELIX Dev Environment..."

# Ensure Python is installed
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3.11+ is required but not found in PATH."
    Return
}

# Create virtual env
Write-Host "Creating virtual environment..."
$env:VENV_DIR=".venv"
if (-not (Test-Path $env:VENV_DIR)) {
    & python -c "import venv; venv.create('.venv', with_pip=True)"
}

# Use python and pip explicitly from the new virtual environment
$VenvPython = "$PWD\.venv\Scripts\python.exe"

# We need to temporarily set PATH to use poetry and pip from venv
$env:Path = "$PWD\.venv\Scripts;$env:Path"

# Install Poetry and dependencies
Write-Host "Installing poetry..."
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install poetry

Write-Host "Installing python dependencies..."
poetry install

# Frontend
Write-Host "Setting up frontend..."
cd frontend
if (Get-Command "npm" -ErrorAction SilentlyContinue) {
    npm install
} else {
    Write-Warning "npm not found. Skipping frontend setup. Please install Node.js."
}
cd ..

Write-Host "Setup complete!"
Write-Host "Run '.venv\Scripts\Activate.ps1' to activate the environment."
