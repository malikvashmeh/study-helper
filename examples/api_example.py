"""
Study Mate Bot - API Usage Example
Demonstrates how to use the API programmatically
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("API is running")
            print(f"📊 Status: {response.json()}")
            return True
        else:
            print(f"API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Make sure the backend server is running.")
        return False

def upload_document(file_path):
    """Upload a document"""
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Document uploaded: {result['filename']}")
            print(f"📄 Chunks created: {result['chunks_created']}")
            print(f"Total documents: {result['total_documents']}")
            return True
        else:
            print(f"Upload failed: {response.text}")
            return False
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"Upload error: {e}")
        return False

def ask_question(question, num_sources=4):
    """Ask a question"""
    try:
        payload = {
            "question": question,
            "num_sources": num_sources
        }
        response = requests.post(f"{API_BASE_URL}/ask", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"❓ Question: {result['question']}")
            print(f"🤖 Answer: {result['answer']}")
            print(f"Sources: {len(result['sources'])} found")
            return result
        else:
            print(f"Question failed: {response.text}")
            return None
    except Exception as e:
        print(f"Question error: {e}")
        return None

def main():
    """Main example function"""
    print("Study Mate Bot - API Example")
    print("=" * 40)
    
    # Check API health
    if not check_api_health():
        return
    
    print("\n" + "=" * 40)
    print("🔄 Example workflow completed!")

if __name__ == "__main__":
    main()
