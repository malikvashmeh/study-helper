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

class BackupRequest(BaseModel):
    backup_name: Optional[str] = None

class RestoreRequest(BaseModel):
    backup_name: str

class RefreshRequest(BaseModel):
    clear_existing: bool = True

class ReplaceDocumentsRequest(BaseModel):
    """Request for replacing all documents with new ones from data folder"""
    force_reprocess: bool = True

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
            # Process document with original filename preserved
            documents = doc_processor.process_document(tmp_file_path, original_filename=file.filename)
            
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

@app.post("/replace-documents")
async def replace_documents(request: ReplaceDocumentsRequest):
    """Replace ALL existing documents with new ones from data folder (complete memory reset + reload)"""
    try:
        # Get components
        doc_processor, vector_store, _ = get_components()
        
        # Create backup before replacing
        backup_name = vector_store.create_backup()
        logger.info(f"Created backup before replacement: {backup_name}")
        
        # Clear processor cache for fresh start
        doc_processor.clear_processed_cache()
        
        # Look for documents in data directory
        data_dir = Path("./data")
        all_new_documents = []
        errors = []
        
        if data_dir.exists():
            for file_path in data_dir.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.docx']:
                    try:
                        documents = doc_processor.process_document(
                            str(file_path), 
                            force_reprocess=request.force_reprocess
                        )
                        if documents:
                            all_new_documents.extend(documents)
                            logger.info(f"Processed: {file_path.name} -> {len(documents)} chunks")
                    except Exception as e:
                        error_msg = f"Error processing {file_path.name}: {str(e)}"
                        errors.append(error_msg)
                        logger.error(error_msg)
        
        # Replace all documents at once
        success = vector_store.replace_all_documents(all_new_documents)
        
        if success:
            return {
                "message": "All documents replaced successfully",
                "new_document_chunks": len(all_new_documents),
                "unique_documents": len(set(doc.metadata.get('document_id', '') for doc in all_new_documents)),
                "errors": errors,
                "backup_created": backup_name,
                "status": "success" if not errors else "partial_success"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to replace documents")
        
    except Exception as e:
        logger.error(f"Error replacing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear-documents")
async def clear_documents():
    """Clear all documents from the vector store (complete memory reset)"""
    try:
        # Get components
        doc_processor, vector_store, _ = get_components()
        
        # Create backup before clearing (safety measure)
        backup_name = vector_store.create_backup()
        
        # Clear vector store completely
        success = vector_store.clear_all_documents()
        
        if success:
            # Clear document processor cache
            doc_processor.clear_processed_cache()
            
            return {
                "message": "All documents and memory cleared completely",
                "backup_created": backup_name,
                "status": "success"
            }
        else:
            return {
                "message": "Failed to clear documents completely",
                "status": "error"
            }
            
    except Exception as e:
        logger.error(f"Error clearing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refresh-documents")
async def refresh_documents(request: RefreshRequest):
    """Refresh the document store (optionally clear and re-process documents from data folder)"""
    try:
        # Get components
        doc_processor, vector_store, _ = get_components()
        
        backup_name = None
        
        if request.clear_existing:
            # Use the new replace method for complete replacement
            return await replace_documents(ReplaceDocumentsRequest(force_reprocess=True))
        else:
            # Just add new documents without clearing
            data_dir = Path("./data")
            processed_count = 0
            errors = []
            
            if data_dir.exists():
                for file_path in data_dir.rglob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.docx']:
                        try:
                            documents = doc_processor.process_document(str(file_path), force_reprocess=False)
                            if documents:
                                vector_store.add_documents(documents)
                                processed_count += len(documents)
                                logger.info(f"Added: {file_path.name}")
                        except Exception as e:
                            error_msg = f"Error processing {file_path.name}: {str(e)}"
                            errors.append(error_msg)
                            logger.error(error_msg)
            
            return {
                "message": "Document refresh completed (additive)",
                "processed_chunks": processed_count,
                "errors": errors,
                "backup_created": backup_name,
                "status": "success" if not errors else "partial_success"
            }
        
    except Exception as e:
        logger.error(f"Error refreshing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/store-stats")
async def get_store_stats():
    """Get vector store statistics and document information"""
    try:
        # Get components
        doc_processor, vector_store, _ = get_components()
        
        # Get comprehensive stats
        stats = vector_store.get_store_stats()
        
        # Add processor info
        processed_docs = doc_processor.get_processed_documents_info()
        stats['processor_cache'] = {
            'cached_documents': len(processed_docs),
            'cache_details': processed_docs
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting store stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-backup")
async def create_backup(request: BackupRequest):
    """Create a backup of the current vector store"""
    try:
        # Get components
        _, vector_store, _ = get_components()
        
        # Create backup
        backup_name = vector_store.create_backup(request.backup_name)
        
        if backup_name:
            return {
                "message": "Backup created successfully",
                "backup_name": backup_name,
                "status": "success"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create backup")
            
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/restore-backup")
async def restore_backup(request: RestoreRequest):
    """Restore vector store from a backup"""
    try:
        # Get components
        doc_processor, vector_store, _ = get_components()
        
        # Restore backup
        success = vector_store.restore_backup(request.backup_name)
        
        if success:
            # Clear processor cache since we restored different data
            doc_processor.clear_processed_cache()
            
            return {
                "message": f"Backup '{request.backup_name}' restored successfully",
                "status": "success"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Backup '{request.backup_name}' not found")
            
    except Exception as e:
        logger.error(f"Error restoring backup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-documents")
async def list_documents():
    """List all documents in the vector store with metadata"""
    try:
        # Get components
        _, vector_store, _ = get_components()
        
        # Get all documents
        all_docs = vector_store.get_all_documents()
        
        # Group by document_id to avoid showing individual chunks
        documents_info = {}
        for doc in all_docs:
            doc_id = doc.metadata.get('document_id', 'unknown')
            
            if doc_id not in documents_info:
                documents_info[doc_id] = {
                    'document_id': doc_id,
                    'filename': doc.metadata.get('filename', 'unknown'),
                    'file_type': doc.metadata.get('file_type', ''),
                    'processing_timestamp': doc.metadata.get('processing_timestamp', ''),
                    'content_hash': doc.metadata.get('content_hash', ''),
                    'total_chunks': doc.metadata.get('total_chunks', 1),
                    'file_size': doc.metadata.get('file_size', 0),
                    'chunks_found': 1
                }
            else:
                documents_info[doc_id]['chunks_found'] += 1
        
        return {
            "documents": list(documents_info.values()),
            "total_unique_documents": len(documents_info),
            "total_chunks": len(all_docs)
        }
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
