# Study Mate Bot - Enterprise RAG System

A powerful Retrieval-Augmented Generation (RAG) system with advanced document management, multi-mode interface, and enterprise-grade reliability. Transform your study materials into an intelligent AI assistant.

![Study Mate Bot](https://img.shields.io/badge/Study%20Mate-Bot-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-red?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Powered-purple?style=for-the-badge)

## Features

### Enterprise-Grade Document Management
- Visual Document Browser with search, filter, and preview capabilities
- Drag & Drop Upload with real-time progress tracking
- Individual Document Management (preview, remove, organize by type)
- Batch Operations (select multiple, bulk remove, bulk upload)
- Smart Memory Management with automatic backups and health verification
- Filename Preservation - no more temporary files or confusing names

### Advanced RAG System
- Multi-Format Support: PDF, TXT, DOCX with intelligent text extraction
- Intelligent Chunking with configurable size and overlap optimization
- Dual Vector Database Support: FAISS (fast) or ChromaDB (advanced features)
- Context-Aware Responses with source citations and metadata
- Duplicate Detection prevents reprocessing of identical content
- Content Hashing for efficient memory management

### 4-Mode User Interface
- Chat Mode: Interactive Q&A with your documents
- Quiz Mode: Generate practice questions and tests
- Summary Mode: Create comprehensive document summaries
- Documents Mode: Complete document management dashboard

### Safety & Reliability Features
- Automatic Backups before every major operation
- Confirmation Dialogs for destructive actions
- Memory Health Testing to verify clean state transitions
- Error Recovery with helpful messages and fallback options
- Atomic Operations with rollback capabilities

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier available)
- 4GB RAM minimum (8GB recommended)
- 2GB storage space

### 2. Installation

#### Option A: One-Command Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/malikvashmeh/study-helper.git
cd study-helper

# Run the automated setup
chmod +x setup.sh
./setup.sh
```

#### Option B: Manual Setup
```bash
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
VECTOR_DB_TYPE=faiss  # or "chroma"
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
streamlit run app.py
```

Visit: **http://localhost:8501**

## Getting Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key
5. Copy the key to your `.env` file

**Note**: The free tier of Gemini API has generous limits and is perfect for personal and educational projects.

## Usage Guide

### Uploading Documents
1. **Quick Upload**: Use the sidebar "Quick Upload" for single documents
2. **Bulk Upload**: Use "Bulk Upload" section for multiple files
3. **Drag & Drop**: Simply drag files into the upload area
4. **File Types**: Supports PDF, TXT, and DOCX files

### Chat with Documents
1. Switch to **Chat Mode**
2. Ask questions about your uploaded documents
3. View source citations for each answer
4. Maintain conversation history across sessions

### Generate Quizzes
1. Switch to **Quiz Mode**
2. Select number of questions (1-10)
3. Choose quiz type (mixed, multiple choice, true/false, short answer)
4. Click "Generate Quiz"
5. Answer questions and reveal correct answers

### Create Summaries
1. Switch to **Summary Mode**
2. Choose summary type (full or section-based)
3. Click "Generate Summary"
4. Get comprehensive document summaries

### Manage Documents
1. Switch to **Documents Mode**
2. Browse all uploaded documents
3. Search and filter by filename or type
4. Preview document content
5. Remove individual or multiple documents
6. View comprehensive statistics

### Memory Management
- **Refresh Documents**: Clear old content and load new documents
- **Reset All Memory**: Complete memory reset with backup
- **Health Check**: Verify that old content has been properly cleared
- **Backup/Restore**: Create and restore document backups

## Architecture

```
study_mate_bot/
├── frontend/              # Streamlit UI
│   └── app.py                # 4-mode interface with document management
├── backend/               # FastAPI server
│   └── main.py               # RESTful API with RAG endpoints
├── utils/                 # Core processing modules
│   ├── document_processor.py # Enhanced document processing with filename preservation
│   ├── vector_store.py       # Advanced vector database management
│   └── llm_manager.py        # LLM integration and conversation memory
├── data/                  # Document storage and vector database
│   ├── documents/           # Your study materials
│   └── vector_db/           # Vector store and backups
└── Documentation         # Comprehensive guides and references
```

## Configuration Options

### Vector Database
- **FAISS** (default): Fast, local vector search, minimal setup
- **ChromaDB**: Advanced features, persistent storage, production-ready

### LLM Providers
- **Google Gemini** (default): Free tier, fast responses, good quality
- **OpenAI GPT** (optional): Premium quality, advanced reasoning

### Document Processing
- **Chunk Size**: 500-1500 characters (default: 1000)
- **Chunk Overlap**: 10-20% of chunk size (default: 200)
- **File Support**: PDF, TXT, DOCX with intelligent extraction

## Performance Characteristics

### Processing Speed
- **Single Document**: < 5 seconds (typical)
- **Batch Upload**: ~2-3 seconds per document
- **Search Response**: < 1 second (typical)
- **Memory Reset**: < 10 seconds with backup

### Storage Efficiency
- **Vector Storage**: ~1MB per 100 document pages
- **Metadata**: Minimal overhead with comprehensive tracking
- **Backups**: Compressed storage format
- **Scalability**: Tested with 1000+ documents

## Use Cases & Applications

### Academic Applications
- **Research Papers**: Upload papers, extract insights, generate summaries
- **Textbook Study**: Chapter-based learning with Q&A
- **Exam Preparation**: Generate practice questions and quizzes
- **Literature Review**: Synthesize multiple sources

### Professional Use
- **Documentation**: Internal knowledge management and search
- **Training Materials**: Employee onboarding and education
- **Research & Development**: Technical documentation analysis
- **Compliance**: Policy and procedure management

### Personal Learning
- **Skill Development**: Structured learning from materials
- **Certification Study**: Focused exam preparation
- **Language Learning**: Text-based language acquisition
- **Hobby Research**: Deep dives into interests

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for APIs
- **LangChain**: RAG framework and document processing
- **FAISS/ChromaDB**: Vector similarity search
- **Google Gemini**: LLM provider with free tier

### Frontend
- **Streamlit**: Interactive web interface
- **Multi-mode UI**: Chat, Quiz, Summary, Documents
- **Real-time Updates**: Live progress and status indicators

### Document Processing
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX processing
- **tiktoken**: Token counting and optimization
- **Content Hashing**: Duplicate detection and memory management

## Supported File Formats

- **PDF**: Text-based PDFs (not scanned images)
- **DOCX**: Microsoft Word documents
- **TXT**: Plain text files

## Example Use Cases

### Research Paper Analysis
1. Upload research papers
2. Ask specific questions about methodology
3. Generate summaries of key findings
4. Create quiz questions for review

### Textbook Study
1. Upload textbook chapters
2. Ask questions about concepts
3. Generate practice quizzes
4. Create comprehensive summaries

### Documentation Management
1. Upload technical documentation
2. Search for specific procedures
3. Generate summaries for new team members
4. Create training materials

## Troubleshooting

### Common Issues

**API Key Error**
```
Error: No Google API key found
```
**Solution**: Ensure your `.env` file contains `GOOGLE_API_KEY=your_key_here`

**Server Connection Error**
```
API server is not running!
```
**Solution**: Start the backend server with `cd backend && python main.py`

**Document Processing Failed**
**Solution**: Ensure documents are not password-protected and are valid formats

**Memory Issues with Large Documents**
**Solution**: Reduce `CHUNK_SIZE` in configuration or process smaller documents

### Performance Tips
- **Optimal Document Size**: 1-50 pages work best
- **Clear Questions**: Specific questions yield better answers
- **Document Quality**: Well-formatted documents produce better results
- **Regular Cleanup**: Use memory management features to maintain performance

## Security & Privacy

- **Local Processing**: Document processing happens locally
- **API Calls**: Only processed chunks are sent to Gemini API
- **No Permanent Storage**: Documents are processed and stored locally
- **Environment Variables**: API keys stored securely in `.env`
- **Backup System**: Automatic backups before major operations

## System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- 2GB storage
- Internet connection (for APIs)

### Recommended Requirements
- Python 3.10+
- 8GB RAM
- 10GB storage
- SSD for better performance

## Future Enhancements

### Planned Features
- **Multi-Language Support**: Process documents in various languages
- **Advanced Search**: Semantic search with filters and metadata
- **Collaboration**: Multi-user document sharing
- **API Integration**: Connect with external services
- **Mobile Interface**: Responsive design for mobile devices

### Technical Improvements
- **Performance Optimization**: Faster processing and search
- **Storage Efficiency**: Better compression and indexing
- **Security Features**: User authentication and permissions
- **Monitoring**: Advanced analytics and usage tracking

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Google Gemini**: For providing the powerful LLM API
- **LangChain**: For the excellent RAG framework
- **FAISS/ChromaDB**: For efficient vector similarity search
- **Streamlit**: For the amazing web framework
- **FastAPI**: For the modern web framework

## Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check the troubleshooting section
- Review the documentation
- Check the PROJECT_INFO.md for detailed technical information

---

**Study Mate Bot combines the power of advanced AI with the simplicity of drag-and-drop document management. No more command-line complexity - just professional results through an intuitive interface.**

**Happy Document Querying!**
