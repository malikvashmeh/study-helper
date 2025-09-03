# Study Mate Bot - Project Information

A comprehensive AI-powered study assistant built with LangChain and Google Gemini, featuring Retrieval-Augmented Generation (RAG) capabilities for document processing, question answering, summarization, and quiz generation.

## Key Features

- **Document Upload & Processing**: Support for PDF, TXT, DOCX files with automatic text extraction and chunking
- **RAG System**: Google Gemini embeddings for document vectors with FAISS/Chroma vector database storage
- **Intelligent Q&A**: Document retrieval and ranking with source citations
- **FastAPI Backend**: Complete REST API with CORS support and error handling
- **Streamlit Frontend**: Interactive UI with chat, quiz, and summary modes
- **Memory & Context**: LangChain conversation memory with session-based context retention
- **Gemini Integration**: Powered by Google Gemini models and embeddings
- **Multiple Vector DBs**: FAISS and Chroma support for different use cases

## Architecture

```
Study Mate Bot/
├── backend/                 # FastAPI backend
│   └── main.py             # Main API server
├── frontend/               # Streamlit frontend
│   └── app.py              # Main UI application
├── utils/                  # Utility modules
│   ├── document_processor.py  # Document processing
│   ├── vector_store.py        # Vector database management
│   └── llm_manager.py         # LLM and memory management
├── data/                   # Data storage
│   └── vector_db/          # Vector database files
├── examples/               # Example usage
│   └── api_example.py      # API usage examples
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── setup.sh               # One-command setup script (RECOMMENDED)
├── run_backend.sh         # Backend startup script
├── run_frontend.sh        # Frontend startup script
├── STARTUP_GUIDE.md       # Quick start guide
└── PROJECT_INFO.md        # This file
```

## Technical Implementation

### Backend (`backend/main.py`)
- **FastAPI Application**: RESTful API with automatic documentation
- **Document Upload**: Multipart file handling with validation
- **RAG Pipeline**: Document processing → Vector storage → Retrieval → LLM generation
- **Memory Management**: Session-based conversation context
- **Error Handling**: Comprehensive error management and logging
- **CORS Support**: Cross-origin resource sharing for frontend integration

### Frontend (`frontend/app.py`)
- **Streamlit Interface**: Modern, responsive UI with sidebar navigation
- **File Upload**: Drag-and-drop document upload with progress indicators
- **Chat Mode**: Real-time conversation with message history
- **Quiz Mode**: Interactive quiz generation and answer checking
- **Summary Mode**: Document summarization with customizable options
- **API Integration**: Seamless communication with backend services

### Utilities

#### `utils/document_processor.py`
- **Multi-format Support**: PDF (PyPDF2), TXT, DOCX (python-docx)
- **Text Chunking**: Configurable chunk size and overlap
- **Metadata Management**: Document source tracking and organization
- **Error Handling**: Robust file processing with fallback mechanisms

#### `utils/vector_store.py`
- **Dual Vector DB Support**: FAISS (fast) and Chroma (feature-rich)
- **Google Embeddings**: Integration with Google Generative AI embeddings
- **Similarity Search**: Configurable search parameters and ranking
- **Persistence**: Automatic saving and loading of vector databases
- **Document Management**: Add, delete, and query document collections

#### `utils/llm_manager.py`
- **Gemini Integration**: Google Generative AI model support
- **Chain Management**: QA, summarization, and quiz generation chains
- **Memory Handling**: Conversation buffer with context retention
- **Prompt Engineering**: Customizable system prompts for different tasks
- **Error Recovery**: Graceful handling of API failures and timeouts

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /upload` - Document upload with multipart form data
- `POST /ask` - Question answering with RAG
- `POST /summarize` - Document summarization
- `POST /quiz` - Quiz generation from documents
- `DELETE /clear-memory` - Clear conversation memory
- `GET /memory-status` - Get memory status and statistics

### Request/Response Examples

#### Upload Document
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.pdf"
```

#### Ask Question
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the main concepts?"}'
```

#### Generate Quiz
```bash
curl -X POST "http://localhost:8000/quiz" \
     -H "Content-Type: application/json" \
     -d '{"num_questions": 5, "quiz_type": "mixed"}'
```

## Configuration Options

### Environment Variables
```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# LLM Configuration
DEFAULT_LLM=gemini
DEFAULT_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=models/embedding-001

# Vector Database
VECTOR_DB_TYPE=faiss
VECTOR_DB_PATH=./data/vector_db

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Server Configuration
BACKEND_PORT=8000
FRONTEND_PORT=8501
LOG_LEVEL=INFO
```

### Vector Database Options
- **FAISS**: Fast similarity search, ideal for smaller datasets
- **Chroma**: More features, better for larger datasets and production

### LLM Models
- **Gemini-1.5-Flash**: Fast, cost-effective for most tasks
- **Gemini-1.5-Pro**: More capable, better for complex reasoning

## 📊 Performance Considerations

### Document Processing
- **Chunk Size**: Larger chunks (1000-2000) for better context, smaller (500-800) for faster processing
- **Overlap**: 10-20% overlap maintains context between chunks
- **File Size**: Recommended max 50MB per document

### Vector Database
- **FAISS**: Best for < 100K documents, faster search
- **Chroma**: Better for > 100K documents, more features

### Memory Management
- **Conversation Buffer**: Automatically manages context
- **Session Persistence**: Maintains state across requests
- **Memory Clearing**: Manual and automatic cleanup options

## Advanced Features

### Custom Prompts
Modify system prompts in `utils/llm_manager.py`:
```python
# Custom QA prompt
qa_prompt = """You are a specialized study assistant for [subject].
Use the provided context to answer questions accurately.
Always cite sources and provide examples when possible."""
```

### Vector Database Migration
Switch between FAISS and Chroma:
```env
# For FAISS (faster)
VECTOR_DB_TYPE=faiss

# For Chroma (more features)
VECTOR_DB_TYPE=chroma
```

### Memory Customization
```python
# Custom memory settings
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)
```

## Fail-Safe and Recovery Options

### Emergency Recovery Commands

#### Complete System Reset
```bash
# Stop all processes
pkill -f "python.*main.py"
pkill -f streamlit
pkill -f uvicorn

# Remove virtual environment and data
rm -rf venv/
rm -rf data/vector_db/
rm -f .env

# Start fresh
./setup.sh
```

#### Port Conflict Resolution
```bash
# Kill processes on specific ports
lsof -ti:8000 | xargs kill -9  # Backend port
lsof -ti:8501 | xargs kill -9  # Frontend port

# Check what's using ports
lsof -i:8000
lsof -i:8501
```

#### Virtual Environment Recovery
```bash
# Remove and recreate venv
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### API Key Troubleshooting
```bash
# Check if API key is set
grep GOOGLE_API_KEY .env

# Test API key manually
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://generativelanguage.googleapis.com/v1beta/models
```

#### Dependency Recovery
```bash
# Update pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Alternative: Use conda
conda create -n study_mate python=3.12
conda activate study_mate
pip install -r requirements.txt
```

#### Vector Database Recovery
```bash
# Remove corrupted vector database
rm -rf data/vector_db/
mkdir -p data/vector_db/

# Restart backend to recreate
./run_backend.sh
```

### Manual Startup (When Scripts Fail)

#### Manual Backend Start
```bash
# Activate virtual environment
source venv/bin/activate

# Start backend manually
cd backend
python3 main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Manual Frontend Start
```bash
# Activate virtual environment
source venv/bin/activate

# Start frontend manually
cd frontend
streamlit run app.py --server.port 8501
```

### Environment Troubleshooting
```bash
# Check all environment variables
cat .env

# Verify Python can see them
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"

# Test environment loading
python3 -c "from dotenv import load_dotenv; load_dotenv(); print('Environment loaded successfully')"
```

### File Permission Recovery
```bash
# Fix script permissions
chmod +x setup.sh
chmod +x run_backend.sh
chmod +x run_frontend.sh

# Fix data directory permissions
chmod -R 755 data/
```

## 🧪 Testing and Development

### Local Development
```bash
# Backend development
cd backend
python main.py

# Frontend development
cd frontend
streamlit run app.py --server.port 8501
```

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Upload test
curl -X POST "http://localhost:8000/upload" \
     -F "file=@test.pdf"

# Question test
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Test question"}'
```

### Comprehensive System Test
```bash
# 1. Test API health
curl -s http://localhost:8000/health | jq

# 2. Test document upload
curl -X POST "http://localhost:8000/upload" \
     -F "file=@test_document.txt"

# 3. Test question answering
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is this document about?"}' | jq

# 4. Test quiz generation
curl -X POST "http://localhost:8000/quiz" \
     -H "Content-Type: application/json" \
     -d '{"num_questions": 3, "quiz_type": "mixed"}' | jq

# 5. Test summarization
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"summary_type": "full"}' | jq
```

## 📈 Scalability and Production

### Production Considerations
- **API Rate Limiting**: Implement rate limiting for API endpoints
- **Database Scaling**: Use external vector databases for large datasets
- **Load Balancing**: Deploy multiple backend instances
- **Monitoring**: Add logging and metrics collection
- **Security**: Implement authentication and authorization

### Deployment Options
- **Docker**: Containerized deployment
- **Cloud Platforms**: AWS, GCP, Azure deployment
- **Serverless**: Function-based deployment
- **Kubernetes**: Container orchestration

## Maintenance and Updates

### Regular Maintenance Tasks
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Clean up old vector databases
rm -rf data/vector_db/old_*

# Check system health
curl http://localhost:8000/health
curl http://localhost:8000/memory-status
```

### Backup and Restore
```bash
# Backup vector database
cp -r data/vector_db/ backup/vector_db_$(date +%Y%m%d)/

# Backup environment
cp .env backup/env_$(date +%Y%m%d)

# Restore from backup
cp -r backup/vector_db_20240101/ data/vector_db/
cp backup/env_20240101 .env
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for functions and classes
- Include error handling and logging

## License

This project is open source and available under the MIT License.

## 🆘 Support and Troubleshooting

### Quick Diagnostics
```bash
# Check system status
ps aux | grep python
lsof -i:8000
lsof -i:8501

# Check logs
tail -f backend.log
tail -f frontend.log

# Test connectivity
curl -v http://localhost:8000/health
curl -v http://localhost:8501
```

### Common Error Solutions

1. **"ModuleNotFoundError"**: Run `pip install -r requirements.txt`
2. **"Port already in use"**: Use port conflict resolution commands
3. **"API key invalid"**: Check and update your Google API key
4. **"Vector database error"**: Use vector database recovery commands
5. **"Permission denied"**: Fix file permissions with chmod commands

For support and questions:
- Check the `STARTUP_GUIDE.md` for quick setup
- Review API documentation at http://localhost:8000/docs
- Use the fail-safe options above
- Open an issue for bugs or feature requests
- Contact the development team

---

**Built with love using LangChain, FastAPI, Streamlit, and Google Gemini**
