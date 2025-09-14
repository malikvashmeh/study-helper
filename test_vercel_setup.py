#!/usr/bin/env python3
"""
Test script to validate Vercel deployment setup
"""
import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import langchain
        print("✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✅ Sentence Transformers imported successfully")
    except ImportError as e:
        print(f"❌ Sentence Transformers import failed: {e}")
        return False
    
    try:
        import faiss
        print("✅ FAISS imported successfully")
    except ImportError as e:
        print(f"❌ FAISS import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "vercel.json",
        "requirements.txt",
        "backend/main.py",
        "frontend/app.py",
        "start_streamlit.py",
        ".env.vercel",
        "DEPLOYMENT_GUIDE.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_vercel_config():
    """Test vercel.json configuration"""
    print("\nTesting vercel.json...")
    
    try:
        import json
        with open("vercel.json", "r") as f:
            config = json.load(f)
        
        required_keys = ["version", "builds", "routes"]
        for key in required_keys:
            if key in config:
                print(f"✅ {key} found in vercel.json")
            else:
                print(f"❌ {key} missing from vercel.json")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Error reading vercel.json: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Vercel Deployment Setup\n")
    
    tests = [
        test_imports,
        test_file_structure,
        test_vercel_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Vercel deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
