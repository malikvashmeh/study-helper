---
title: Study Mate Bot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.1
app_file: app.py
pinned: false
license: mit
short_description: AI-powered study assistant with RAG capabilities
---

# Study Mate Bot

An intelligent study assistant powered by LangChain and local embeddings. Upload documents, ask questions, generate quizzes, and get AI-powered summaries.

## Features

- 📄 **Document Upload**: Support for PDF, TXT, and DOCX files
- 💬 **AI Chat**: Ask questions about your uploaded documents
- 🧠 **Local Embeddings**: No API costs for document processing
- 📝 **Quiz Generation**: Create quizzes from your documents
- 📊 **Text Summarization**: Get AI-powered summaries
- 🔄 **Persistent Memory**: Chat history within sessions

## How to Use

1. **Upload Documents**: Use the document upload section to add your study materials
2. **Ask Questions**: Chat with the AI about your uploaded content
3. **Generate Quizzes**: Create practice quizzes from your documents
4. **Get Summaries**: Summarize any text or document content

## Technical Details

- **Backend**: FastAPI with local embeddings
- **Frontend**: Streamlit with modern UI
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS for fast similarity search
- **LLM**: Google Gemini for chat and generation

## Environment Variables

Set these in your Hugging Face Spaces secrets:

- `GOOGLE_API_KEY`: Your Google Gemini API key
- `OPENAI_API_KEY`: (Optional) OpenAI API key for fallback

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will start both the FastAPI backend (port 8000) and Streamlit frontend (port 7860).
