"""
Study Mate Bot - FastAPI Backend for Vercel Deployment
Main API server with RAG functionality and Streamlit frontend serving
"""

import os
import logging
import tempfile
import subprocess
import threading
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# FastAPI imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Local imports
import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils.document_processor import DocumentProcessor
from utils.vector_store import VectorStoreManager
from utils.llm_manager import LLMManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Study Mate Bot API",
    description="RAG-powered study assistant with document processing and Q&A",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
document_processor = None
vector_store = None
llm_manager = None
streamlit_process = None

def start_streamlit_subprocess():
    """Start Streamlit as a subprocess"""
    global streamlit_process
    try:
        # Path to the frontend directory
        frontend_dir = Path(__file__).parent.parent / "frontend"
        
        # Command to start Streamlit
        cmd = [
            "python", "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        logger.info(f"Starting Streamlit subprocess in {frontend_dir}")
        streamlit_process = subprocess.Popen(
            cmd,
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        if streamlit_process.poll() is None:
            logger.info("Streamlit started successfully")
        else:
            stdout, stderr = streamlit_process.communicate()
            logger.error(f"Streamlit failed to start: {stderr.decode()}")
            
    except Exception as e:
        logger.error(f"Error starting Streamlit: {e}")

def get_components():
    """Get or initialize components"""
    global document_processor, vector_store, llm_manager
    
    if document_processor is None:
        # Initialize document processor
        document_processor = DocumentProcessor()
        
        # Initialize vector store
        vector_store = VectorStoreManager(
            embedding_model=os.getenv("EMBEDDING_PROVIDER", "local"),
            embedding_model_name=os.getenv("HF_EMBEDDING_MODEL", "models/embedding-001"),
            vector_db_type=os.getenv("VECTOR_DB_TYPE", "faiss"),
            vector_db_path=os.getenv("VECTOR_DB_PATH", "./data/vector_db")
        )
        
        # Initialize LLM manager
        llm_manager = LLMManager(
            llm_provider=os.getenv("DEFAULT_LLM", "gemini"),
            model_name=os.getenv("DEFAULT_MODEL", "gemini-1.5-flash"),
            temperature=0.7,
            max_tokens=1000
        )
    
    return document_processor, vector_store, llm_manager

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    try:
        get_components()
        
        # Start Streamlit in a separate thread
        streamlit_thread = threading.Thread(target=start_streamlit_subprocess, daemon=True)
        streamlit_thread.start()
        
        logger.info("Study Mate Bot API started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint - redirect to Streamlit UI"""
    return RedirectResponse(url="/ui")

@app.get("/ui")
async def streamlit_ui():
    """Serve Streamlit UI via iframe"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Study Mate Bot</title>
        <style>
            body { margin: 0; padding: 0; }
            iframe { 
                width: 100vw; 
                height: 100vh; 
                border: none; 
            }
        </style>
    </head>
    <body>
        <iframe src="http://localhost:8501" width="100%" height="100%"></iframe>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Study Mate Bot API",
        "version": "1.0.0",
        "status": "running",
        "streamlit_ui": "/ui"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

# Include all the existing API endpoints from the original main.py
# (Upload, chat, quiz, summary endpoints remain the same)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_types = ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Get components
        doc_processor, vector_store, _ = get_components()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Process document with original filename preserved
            documents = doc_processor.process_document(tmp_file_path, original_filename=file.filename)
            
            if not documents:
                raise HTTPException(status_code=400, detail="No content extracted from document")
            
            # Add to vector store
            vector_store.add_documents(documents)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            return {
                "message": f"Document '{file.filename}' processed successfully",
                "chunks": len(documents),
                "filename": file.filename
            }
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
            raise e
            
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer"""
    try:
        # Get components
        _, vector_store, llm_manager = get_components()
        
        # Search for relevant documents
        similar_docs = vector_store.search_documents(request.question, k=3)
        
        if not similar_docs:
            return {"answer": "No relevant documents found. Please upload some documents first."}
        
        # Create context from similar documents
        context = "\n\n".join([doc.page_content for doc in similar_docs])
        
        # Get answer from LLM
        answer = llm_manager.answer_question(request.question, context)
        
        return {"answer": answer}
        
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class QuizRequest(BaseModel):
    text: str
    num_questions: int = 5

@app.post("/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate quiz questions from text"""
    try:
        # Get components
        _, _, llm_manager = get_components()
        
        # Generate quiz
        quiz = llm_manager.generate_quiz(request.text, request.num_questions)
        
        return quiz
        
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class SummaryRequest(BaseModel):
    text: str

@app.post("/summary")
async def summarize_text(request: SummaryRequest):
    """Summarize provided text"""
    try:
        # Get components
        _, _, llm_manager = get_components()
        
        # Generate summary
        summary = llm_manager.summarize_text(request.text)
        
        return {"summary": summary}
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
