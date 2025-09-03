#!/bin/bash

# Study Mate Bot - Backend Startup Script

echo "Starting Study Mate Bot Backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo ".env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
mkdir -p data/vector_db

# Start the backend server
echo "Starting FastAPI server..."
cd backend
python3 main.py
