"""
Study Mate Bot - Hugging Face Spaces Entry Point
Main launcher that starts both FastAPI backend and Streamlit frontend
"""

import os
import sys
import subprocess
import threading
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_fastapi_backend():
    """Start FastAPI backend in a separate thread"""
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent / "backend"
        
        # Start FastAPI with uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ]
        
        logger.info(f"Starting FastAPI backend in {backend_dir}")
        process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for FastAPI to start
        time.sleep(3)
        
        if process.poll() is None:
            logger.info("FastAPI backend started successfully on port 8000")
            return process
        else:
            stdout, stderr = process.communicate()
            logger.error(f"FastAPI failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        logger.error(f"Error starting FastAPI backend: {e}")
        return None

def main():
    """Main entry point for Hugging Face Spaces"""
    logger.info("Starting Study Mate Bot on Hugging Face Spaces...")
    
    # Start FastAPI backend in background
    backend_process = start_fastapi_backend()
    
    if backend_process is None:
        logger.error("Failed to start FastAPI backend. Exiting.")
        sys.exit(1)
    
    # Wait a moment for backend to be ready
    time.sleep(2)
    
    # Import and run Streamlit
    try:
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        # Import streamlit and run the app
        import streamlit.web.cli as stcli
        import sys
        
        # Set up Streamlit arguments
        sys.argv = [
            "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "7860",  # HF Spaces default port
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        logger.info("Starting Streamlit frontend...")
        stcli.main()
        
    except Exception as e:
        logger.error(f"Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
