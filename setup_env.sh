#!/bin/bash
# HELIX Virtual Environment Setup Script

echo "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing poetry..."
pip install poetry

echo "Installing dependencies..."
poetry install

echo "Setting up frontend..."
cd frontend && npm install && cd ..

echo "Environment setup complete."
