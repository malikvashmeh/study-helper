#!/bin/bash

# Study Mate Bot - Frontend Startup Script

echo "Starting Study Mate Bot Frontend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run ./run_backend.sh first to set up the environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start the frontend
echo "Starting Streamlit app..."
cd frontend
streamlit run app.py
