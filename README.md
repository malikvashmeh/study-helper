# 📚 Study Mate Bot

**AI-powered study assistant with document management and Q&A capabilities**

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher

### 2. Get API Keys
**Google Gemini (for chat):**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key

**OpenAI (for embeddings - recommended):**
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in with your OpenAI account
3. Click "Create new secret key"
4. Copy the key

### 3. Configuration
Copy the example file and add your API keys:
```bash
cp .env.example .env
```

Then edit `.env` with your keys:
```env
# Google Gemini API (for chat)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI API (for embeddings - recommended)
OPENAI_API_KEY=your_openai_api_key_here

# Configuration
DEFAULT_LLM=gemini
DEFAULT_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=openai
EMBEDDING_MODEL_NAME=text-embedding-3-small
VECTOR_DB_TYPE=faiss
VECTOR_DB_PATH=./data/vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
./run_backend.sh
```
*This script automatically:*
- Creates virtual environment
- Installs all dependencies
- Sets up data directories
- Starts the backend server

**Terminal 2 - Frontend:**
```bash
./run_frontend.sh
```
*This script automatically:*
- Activates the virtual environment
- Starts the frontend interface

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

### API rate limit errors?
**If you see "429 You exceeded your current quota" error:**

**Option 1 - Wait for reset:**
- Google's free tier resets daily at midnight Pacific Time
- Wait 24 hours and try again

**Option 2 - Use smaller documents:**
- Upload smaller PDFs (1-5 pages)
- Split large documents into smaller files
- This reduces API calls needed

**Option 3 - Switch to OpenAI embeddings:**
- Get OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Add `OPENAI_API_KEY=your_key_here` to `.env` file
- Set `EMBEDDING_MODEL=openai` in `.env` file
- Restart the application

### Backend won't start?
- Make sure you have a `.env` file with your API keys
- Check that Python 3.8+ is installed
- The script will create everything else automatically

### Frontend shows connection error?
```bash
# Verify backend is running
curl http://localhost:8000/health
# Should return: {"status": "healthy", "message": "API is running"}
```

### Documents not uploading?
- Check file format: Only PDF, TXT, DOCX supported
- Check file size: Large files need more time
- Check backend terminal for error messages

### Old content still appearing?
1. Documents Mode → "Clear All" → Confirm
2. Upload your new documents
3. Run "Test Memory" to verify clean state

## 📋 Requirements

See `requirements.txt` for complete dependency list.

## 🔧 Scripts

- `run_backend.sh` - Sets up environment and starts backend
- `run_frontend.sh` - Starts frontend (run backend first)

---

**Happy Studying! 🎉**
