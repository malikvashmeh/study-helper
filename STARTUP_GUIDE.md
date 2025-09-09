# 🚀 Quick Start Guide

Get your Study Mate Bot running in 5 minutes with the enhanced document management interface!

## ⚡ Fast Setup

### 1. First-Time Setup
```bash
# Make setup script executable and run
chmod +x setup.sh
./setup.sh

# This will:
# - Create virtual environment
# - Install all dependencies
# - Set up directory structure
```

### 2. Configure API Keys
Create `.env` file in project root:
```env
# Required: Google Gemini API (free tier available)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: OpenAI API
OPENAI_API_KEY=your_openai_key_here
```

**🔑 Get Google API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy and paste into `.env` file

### 3. Launch Application
```bash
# Terminal 1: Start Backend
./run_backend.sh

# Terminal 2: Start Frontend
./run_frontend.sh
```

**🌐 Access Points:**
- **Frontend Interface**: http://localhost:8501 (your main interface)
- **API Documentation**: http://localhost:8000/docs (advanced users)

## 🎯 First Steps with Enhanced Interface

### 1. Upload Your First Documents
1. **Open the frontend** at http://localhost:8501
2. **Click "Documents" tab** for full management interface
3. **Upload documents** using:
   - **Quick Upload** (sidebar): Single file drag & drop
   - **Bulk Upload** (sidebar): Multiple files at once
   - **Documents Mode**: Advanced management dashboard

### 2. Chat with Your Documents
1. **Switch to "Chat" tab**
2. **Ask questions** like:
   - "What are the main topics covered?"
   - "Summarize the key points from Chapter 3"
   - "What does the document say about [specific topic]?"
3. **View sources** in the expandable source sections

### 3. Generate Study Materials
- **Quiz Mode**: Create practice questions from your documents
- **Summary Mode**: Generate comprehensive summaries
- **Documents Mode**: Browse, search, and manage your knowledge base

## 🛠️ Interface Overview

### **Enhanced Sidebar Controls**
- **📄 Quick Upload**: Instant single-file addition
- **📁 Document Manager**: Visual document browser (toggle)
- **📂 Bulk Upload**: Multi-file upload with modes:
  - "Add to Current" - Keep existing, add new
  - "Replace All" - Fresh start with new documents
- **🧠 Memory Management**: Complete system controls

### **Four Main Modes**
1. **💬 Chat**: Q&A with your documents
2. **🧠 Quiz**: Generate practice questions  
3. **📋 Summary**: Create document summaries
4. **📁 Documents**: Full document management center

## 📊 Documents Mode Dashboard

Your command center for document management:

- **📈 Statistics**: Document counts, file types, storage info
- **🔍 Search & Filter**: Find specific documents quickly
- **👁️ Preview**: View document content before decisions
- **⚡ Bulk Operations**: Refresh all, clear all, create backups
- **🩺 Health Check**: Verify memory is clean after updates

## 🎓 Pro Tips for Best Experience

### **Document Management**
- **Organize files** in `data/documents/` folder for batch operations
- **Use descriptive filenames** - they're now preserved!
- **Regular cleanup** - use "Refresh Documents" when adding new materials
- **Test memory** after major changes to ensure clean updates

### **Asking Better Questions**
- **Be specific**: "What is photosynthesis?" vs "Explain biology"
- **Reference documents**: "According to Chapter 2, how does..."
- **Build conversations**: Ask follow-up questions for deeper understanding
- **Check sources**: Always verify citations in responses

### **Memory Management**
- **Before major updates**: Create manual backup in Documents Mode
- **After uploading new content**: Run memory health test
- **Regular maintenance**: Use "Refresh All" periodically
- **Clean slate needed**: Use "RESET ALL MEMORY" with double-click confirmation

## ⚠️ Troubleshooting

### **Quick Fixes**

**🔧 Backend won't start?**
```bash
# Check virtual environment
source venv/bin/activate
pip install -r requirements.txt

# Try manual start
cd backend && python main.py
```

**🔧 Frontend shows connection error?**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", "message": "API is running"}
```

**🔧 Old content still appearing?**
```bash
# Use complete memory reset
1. Documents Mode → "Clear All" → Confirm
2. Upload your new documents
3. Run "Test Memory" to verify clean state
```

**🔧 Documents not uploading?**
- **Check file format**: Only PDF, TXT, DOCX supported
- **Check file size**: Large files need more time
- **Check filename**: Special characters may cause issues
- **Check logs**: Backend terminal shows detailed errors

### **Advanced Options**

**🔧 Switch vector database:**
Edit `backend/main.py` - change `VECTOR_DB_TYPE` environment variable to "chroma" for advanced features.

**🔧 Adjust chunking:**
Edit `utils/document_processor.py` - modify `chunk_size` and `chunk_overlap` parameters.

**🔧 Change LLM provider:**
Edit environment variables in `.env` file and update `backend/main.py` configuration.

## 🎉 You're Ready!

Your Study Mate Bot now features:
- ✅ **Professional document management** - no more command-line needed
- ✅ **Filename preservation** - your original names are kept
- ✅ **Visual interface** - browse, search, preview documents
- ✅ **Safety features** - backups, confirmations, health checks
- ✅ **Enterprise reliability** - memory management and error recovery

**🌐 Start studying: http://localhost:8501**

Need help? Check the full README.md or browse Documents Mode for comprehensive management options!
