# Vercel Deployment Guide

## 🚀 Deploy Study Mate Bot to Vercel

This guide will help you deploy your full-stack Study Mate Bot application to Vercel.

### 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **API Keys**: Get your Google Gemini API key

### 🔧 Setup Steps

#### 1. Environment Variables

Set these environment variables in your Vercel dashboard:

```bash
# Google Gemini API (for chat)
GOOGLE_API_KEY=your_actual_google_api_key

# OpenAI API (optional fallback)
OPENAI_API_KEY=your_openai_api_key

# Configuration
DEFAULT_LLM=gemini
DEFAULT_MODEL=gemini-1.5-flash

# Local Embeddings (Primary)
EMBEDDING_PROVIDER=local
EMBEDDINGS_CACHE_PATH=data/embeddings_cache.pkl
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Vector Database
VECTOR_DB_TYPE=faiss
VECTOR_DB_PATH=./data/vector_db

# Document Processing
CHUNK_SIZE=1800
CHUNK_OVERLAP=100

# Vercel specific
PYTHONPATH=.
```

#### 2. Deploy to Vercel

**Option A: Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name: study-mate-bot
# - Directory: ./
# - Override settings? No
```

**Option B: GitHub Integration**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect it's a Python project
5. Set environment variables in the dashboard
6. Click "Deploy"

### 🌐 Access Your App

After deployment, you'll get a URL like:
- **Main App**: `https://your-app.vercel.app/`
- **Streamlit UI**: `https://your-app.vercel.app/ui`
- **API Docs**: `https://your-app.vercel.app/docs`

### 🔍 How It Works

1. **FastAPI Backend**: Serves as the main serverless function
2. **Streamlit Subprocess**: Runs in headless mode on port 8501
3. **Iframe Integration**: Streamlit UI is embedded via iframe at `/ui`
4. **API Endpoints**: All your existing APIs work at `/api/*`

### 📁 File Structure

```
study_mate_bot/
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── .env.vercel             # Environment template
├── start_streamlit.py      # Streamlit startup script
├── backend/
│   └── main.py            # Modified FastAPI app
├── frontend/
│   └── app.py             # Streamlit UI (unchanged)
└── utils/                 # Supporting modules
```

### 🛠️ Troubleshooting

**Issue**: Streamlit not loading
- **Solution**: Check that port 8501 is available and Streamlit process started

**Issue**: API key errors
- **Solution**: Verify environment variables are set correctly in Vercel dashboard

**Issue**: Import errors
- **Solution**: Ensure `PYTHONPATH=.` is set in environment variables

**Issue**: Memory issues
- **Solution**: Vercel has memory limits; consider optimizing model loading

### 🔄 Updates

To update your deployment:
```bash
# Push changes to GitHub
git add .
git commit -m "Update app"
git push

# Vercel will auto-deploy
# Or manually trigger:
vercel --prod
```

### 📊 Monitoring

- **Logs**: Check Vercel dashboard for function logs
- **Performance**: Monitor function execution time
- **Errors**: Set up error tracking in Vercel

### 🎯 Features Available

✅ **Document Upload**: PDF, TXT, DOCX support
✅ **Chat Interface**: AI-powered Q&A
✅ **Quiz Generation**: Create quizzes from documents
✅ **Text Summarization**: Summarize any text
✅ **Local Embeddings**: No API costs for embeddings
✅ **Persistent Memory**: Chat history within sessions

### 🚨 Important Notes

1. **Cold Starts**: First request may be slower due to model loading
2. **Memory Limits**: Vercel has memory constraints for large models
3. **Timeout**: Functions have execution time limits
4. **Persistence**: Data is not persistent between deployments

### 🆘 Support

If you encounter issues:
1. Check Vercel function logs
2. Verify environment variables
3. Test locally first
4. Check the deployment guide

Happy deploying! 🎉
