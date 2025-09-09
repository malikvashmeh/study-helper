#!/bin/bash

# Study Mate Bot - One-Command Setup Script (Gemini Only)

echo "Setting up Study Mate Bot (Gemini Only)..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created!"
    echo ""
    echo "IMPORTANT: You need to edit .env and add your Google API key:"
    echo "   - GOOGLE_API_KEY (required)"
    echo ""
    echo "   Get Google key: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your Google API key to .env..."
fi

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo "�� Virtual environment already exists, skipping creation..."
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Trying with 'python'..."
        python -m venv venv
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment. Please check your Python installation."
            exit 1
        fi
    fi
    echo "Virtual environment created!"
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Please check your internet connection and try again."
    exit 1
fi

# Create data directory
echo "📁 Creating data directories..."
mkdir -p data/vector_db

echo ""
echo "Setup complete!"
echo ""
echo "IMPORTANT: To activate the virtual environment in your current shell, run:"
echo "   source venv/bin/activate"
echo ""
echo "To run the application:"
echo "   Terminal 1: ./run_backend.sh"
echo "   Terminal 2: ./run_frontend.sh"
echo ""
echo "🌐 Then visit: http://localhost:8501"
echo ""
echo "Happy studying!"
