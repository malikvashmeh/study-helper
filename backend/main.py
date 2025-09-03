"""
Study Mate Bot - FastAPI Backend
Main API server with RAG functionality
"""

import os
import logging
import tempfile
from typing import List, Dict, Any, Optional
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# FastAPI imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
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

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

class SummaryRequest(BaseModel):
    summary_type: str = "full"

class QuizRequest(BaseModel):
    summary_type: str = "full"
    num_questions: int

# Dependency to initialize components
def get_components():
    global document_processor, vector_store, llm_manager
    
    if document_processor is None:
        document_processor = DocumentProcessor(
            chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 200))
        )
    
    if vector_store is None:
        vector_store = VectorStoreManager(
            vector_db_type=os.getenv("VECTOR_DB_TYPE", "faiss"),
            vector_db_path=os.getenv("VECTOR_DB_PATH", "./data/vector_db"),
            embedding_model="google",  # Default to Google
            embedding_model_name=os.getenv("EMBEDDING_MODEL", "models/embedding-001")
        )
    
    if llm_manager is None:
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
        logger.info("Study Mate Bot API started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Study Mate Bot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

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
            # Process document
            documents = doc_processor.process_document(tmp_file_path)
            
            # Add to vector store
            vector_store.add_documents(documents)
            
            return {
                "message": f"Document '{file.filename}' uploaded and processed successfully",
                "chunks": len(documents),
                "filename": file.filename
            }
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded documents"""
    try:
        # Get components
        _, vector_store, llm_manager = get_components()
        
        # Search for relevant documents
        relevant_docs = vector_store.similarity_search(request.question, k=4)
        
        if not relevant_docs:
            return {
                "answer": "No relevant documents found. Please upload some documents first.",
                "sources": []
            }
        
        # Combine context from relevant documents
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Generate answer
        answer = llm_manager.answer_question(request.question, context)
        
        # Prepare sources
        sources = [{"content": doc.page_content[:200] + "...", "metadata": doc.metadata} for doc in relevant_docs]
        
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize_document(request: SummaryRequest):
    """Summarize provided text"""
    try:
        # Get components
        _, _, llm_manager = get_components()
        
        # Generate summary
        # Get all documents from vector store
        all_docs = vector_store.get_all_documents()
        if not all_docs:
            raise HTTPException(status_code=400, detail="No documents uploaded. Please upload documents first.")
        
        # Combine all document content
        combined_text = "\n\n".join([doc.page_content for doc in all_docs])
        
        # Generate summary
        summary = llm_manager.summarize_text(combined_text)
        
        return {
            "summary": summary,
            "original_length": len(combined_text),
            "summary_length": len(summary)
        }
        
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate quiz questions from text"""
    try:
        # Get components
        _, _, llm_manager = get_components()
        
        # Generate quiz
        # Get all documents from vector store
        all_docs = vector_store.get_all_documents()
        if not all_docs:
            raise HTTPException(status_code=400, detail="No documents uploaded. Please upload documents first.")
        
        # Combine all document content
        combined_text = "\n\n".join([doc.page_content for doc in all_docs])
        
        # Generate quiz
        quiz = llm_manager.generate_quiz(combined_text, request.num_questions)
        
        return {
            "questions": quiz.get("questions", []),
            "num_questions": request.num_questions
        }
        
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear-memory")
async def clear_memory():
    """Clear conversation memory"""
    try:
        # Get components
        _, _, llm_manager = get_components()
        
        # Clear memory
        llm_manager.clear_memory()
        
        return {"message": "Memory cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory-status")
async def memory_status():
    """Get memory status"""
    try:
        # Get components
        _, _, llm_manager = get_components()
        
        # Get memory summary
        summary = llm_manager.get_memory_summary()
        
        return {"memory_status": summary}
        
    except Exception as e:
        logger.error(f"Error getting memory status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
