# Study Mate Bot - Startup Guide

## ⚡ Super Quick Start (1 Command!)

### Option 1: One-Command Setup (Recommended)
```bash
./setup.sh
```
This automatically:
- Creates `.env` file from template
- Sets up virtual environment
- Installs all dependencies
- Creates necessary directories
- Guides you through adding your Google API key

**Then just run:**
```bash
# Terminal 1: Start Backend
./run_backend.sh

# Terminal 2: Start Frontend
./run_frontend.sh
```

## ⚡ Manual Setup (3 Steps)

### 1. Set Up Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your Google API key (REQUIRED!)
nano .env
```

**Required API Key:**
- `GOOGLE_API_KEY` - Get from https://makersuite.google.com/app/apikey

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Terminal 1: Start Backend
./run_backend.sh

# Terminal 2: Start Frontend
./run_frontend.sh
```

## 🌐 Access Your App
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## What You Can Do
1. **Upload Documents** - PDF, TXT, DOCX files
2. **Ask Questions** - Get AI answers with source citations
3. **Generate Quizzes** - Multiple choice, true/false questions
4. **Create Summaries** - Comprehensive document summaries

## Configuration Options

Edit `.env` to customize:

```env
# LLM Settings (Gemini only)
DEFAULT_LLM=gemini
DEFAULT_MODEL=gemini-1.5-flash  # or gemini-1.5-pro

# Vector Database
VECTOR_DB_TYPE=faiss        # or chroma
VECTOR_DB_PATH=./data/vector_db

# Document Processing
CHUNK_SIZE=1000            # Size of text chunks
CHUNK_OVERLAP=200          # Overlap between chunks

# Embeddings (Google only)
EMBEDDING_MODEL=models/embedding-001
```

## Fail-Safe Options

### If Something Goes Wrong:

#### 1. **Port Conflicts**
```bash
# Kill processes on ports 8000 and 8501
pkill -f "python.*main.py"
pkill -f streamlit
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Then restart
./run_backend.sh
./run_frontend.sh
```

#### 2. **Virtual Environment Issues**
```bash
# Remove and recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. **API Key Problems**
```bash
# Check if API key is set
grep GOOGLE_API_KEY .env

# Test API key manually
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://generativelanguage.googleapis.com/v1beta/models
```

#### 4. **Vector Database Corruption**
```bash
# Clear vector database (WARNING: Deletes all uploaded documents)
rm -rf data/vector_db/*
mkdir -p data/vector_db
```

#### 5. **Dependency Issues**
```bash
# Fresh install
pip uninstall -r requirements.txt -y
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. **Manual Backend Start (If Scripts Fail)**
```bash
# Activate venv manually
source venv/bin/activate

# Start backend manually
cd backend
python3 main.py
```

#### 7. **Manual Frontend Start (If Scripts Fail)**
```bash
# Activate venv manually
source venv/bin/activate

# Start frontend manually
cd frontend
streamlit run app.py --server.port 8501
```

#### 8. **Reset Everything (Nuclear Option)**
```bash
# Complete reset
rm -rf venv
rm -rf data/vector_db
rm .env
./setup.sh
```

## 🐛 Troubleshooting

### Common Issues:

1. **"API server not running"**
   - Make sure backend is running on port 8000
   - Check terminal for error messages
   - Try fail-safe option #1 (Port Conflicts)

2. **"API key errors"**
   - Verify your Google API key in `.env` file
   - Ensure you have sufficient API credits
   - Try fail-safe option #3 (API Key Problems)

3. **"Import errors"**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)
   - Try fail-safe option #5 (Dependency Issues)

4. **"Document upload fails"**
   - Check file format (PDF, TXT, DOCX only)
   - Ensure file is not corrupted
   - Try fail-safe option #4 (Vector Database Corruption)

5. **"Virtual environment not found"**
   - Try fail-safe option #2 (Virtual Environment Issues)
   - Or fail-safe option #8 (Reset Everything)

6. **"Scripts don't work"**
   - Try fail-safe options #6 and #7 (Manual Start)
   - Check file permissions: `chmod +x *.sh`

## 🧪 Test the API

```bash
# Test API health
curl http://localhost:8000/health

# Upload a document
curl -X POST "http://localhost:8000/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.pdf"

# Ask a question
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is this document about?"}'
```

## 🆘 Emergency Recovery

If nothing works:

1. **Check system requirements:**
   ```bash
   python3 --version  # Should be 3.8+
   pip --version      # Should be recent
   ```

2. **Verify file permissions:**
   ```bash
   ls -la *.sh        # Should show executable permissions
   chmod +x *.sh      # Make scripts executable
   ```

3. **Check disk space:**
   ```bash
   df -h              # Ensure sufficient space
   ```

4. **Network connectivity:**
   ```bash
   ping google.com    # Test internet connection
   ```

5. **Last resort - Complete reinstall:**
   ```bash
   # Backup your .env file
   cp .env .env.backup
   
   # Remove everything
   rm -rf venv data/vector_db
   
   # Fresh start
   ./setup.sh
   
   # Restore your API key
   cp .env.backup .env
   ```

## 🆘 Need Help?
- Check the full `PROJECT_INFO.md` for detailed documentation
- Review the API documentation at http://localhost:8000/docs
- Make sure your Google API key is valid and has credits
- Try the fail-safe options above
- Check system logs for detailed error messages

---
**Happy Studying!**
