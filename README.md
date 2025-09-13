# 📚 Study Mate Bot

**AI-powered study assistant with document management and Q&A capabilities**

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher

### 2. Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key

### 3. Configuration
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
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

### Backend won't start?
- Make sure you have a `.env` file with your Google API key
- Check that Python 3.8+ is installed
- The script will create everything else automatically

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
