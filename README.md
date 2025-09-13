# 📚 Study Mate Bot

**AI-powered study assistant with document management and Q&A capabilities**

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier available)

### 2. Setup
```bash
# Clone and setup
git clone <your-repo-url>
cd study_mate_bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Create data directories
mkdir -p data/vector_db
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
OPENAI_API_KEY=your_openai_key_here
VECTOR_DB_TYPE=faiss
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key
5. Copy the key to your `.env` file

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
./run_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./run_frontend.sh
```

**Access:** http://localhost:8501

## 📖 Usage

### Upload Documents
- Use the sidebar "Quick Upload" for single documents
- Use "Bulk Upload" for multiple files
- Supports PDF, TXT, and DOCX files

### Chat with Documents
- Switch to "Chat Mode"
- Ask questions about your uploaded documents
- View source citations for each answer

### Generate Quizzes
- Switch to "Quiz Mode"
- Select number of questions (1-10)
- Choose quiz type (mixed, multiple choice, true/false, short answer)

### Create Summaries
- Switch to "Summary Mode"
- Choose summary type (full or section-based)
- Generate comprehensive document summaries

### Manage Documents
- Switch to "Documents Mode"
- Browse, search, and filter documents
- Preview content and remove documents

## 🛠️ Troubleshooting

### Backend won't start?
```bash
# Check virtual environment
source venv/bin/activate
pip install -r requirements.txt

# Try manual start
cd backend && python main.py
```

### Frontend shows connection error?
```bash
# Verify backend is running
curl http://localhost:8000/health

# Should return: {"status": "healthy", "message": "API is running"}
```

### API rate limit errors?
- Google's free tier has daily limits (1,000 requests/day)
- Wait 24 hours for quota reset
- Consider using smaller documents
- Switch to OpenAI embeddings for higher limits

### Documents not uploading?
- Check file format: Only PDF, TXT, DOCX supported
- Check file size: Large files need more time
- Check filename: Special characters may cause issues
- Check logs: Backend terminal shows detailed errors

### Old content still appearing?
```bash
# Use complete memory reset
1. Documents Mode → "Clear All" → Confirm
2. Upload your new documents
3. Run "Test Memory" to verify clean state
```

## 📋 Requirements

See `requirements.txt` for complete dependency list.

## 🔧 Scripts

- `run_backend.sh` - Start the FastAPI backend server
- `run_frontend.sh` - Start the Streamlit frontend
- `setup.sh` - Automated setup script

## 📁 Project Structure

```
study_mate_bot/
├── frontend/          # Streamlit UI
├── backend/           # FastAPI server
├── utils/             # Core processing modules
├── data/              # Document storage
└── requirements.txt   # Dependencies
```

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check that both backend and frontend are running

---

**Happy Studying! 🎉**
