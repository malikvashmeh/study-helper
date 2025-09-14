#!/usr/bin/env python3
"""
Streamlit startup script for Vercel deployment.
Runs Streamlit in headless mode as a subprocess.
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def start_streamlit():
    """Start Streamlit app in headless mode"""
    try:
        # Change to frontend directory
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        
        # Start Streamlit in headless mode
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        print(f"Starting Streamlit with command: {' '.join(cmd)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        if process.poll() is None:
            print("Streamlit started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"Streamlit failed to start: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        return None

if __name__ == "__main__":
    start_streamlit()
