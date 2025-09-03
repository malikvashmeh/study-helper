"""
Vector Store Management
Handles FAISS and Chroma vector databases with Gemini embeddings
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Vector database imports
import faiss
import numpy as np
import chromadb
from chromadb.config import Settings

# LangChain imports
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS, Chroma

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages vector database operations"""
    
    def __init__(self, 
                 vector_db_type: str = "faiss",
                 vector_db_path: str = "./data/vector_db",
                 embedding_model: str = "google",
                 embedding_model_name: str = "models/embedding-001"):
        
        self.vector_db_type = vector_db_type.lower()
        self.vector_db_path = Path(vector_db_path)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = self._initialize_embeddings(embedding_model, embedding_model_name)
        
        # Initialize vector store
        self.vector_store = self._initialize_vector_store()
    
    def _initialize_embeddings(self, embedding_model: str, model_name: str):
        """Initialize embedding model"""
        if embedding_model.lower() == "google":
            return GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported embedding model: {embedding_model}. Only 'google' is supported.")
    
    def _initialize_vector_store(self):
        """Initialize vector store based on type"""
        if self.vector_db_type == "faiss":
            return self._initialize_faiss()
        elif self.vector_db_type == "chroma":
            return self._initialize_chroma()
        else:
            raise ValueError(f"Unsupported vector DB type: {self.vector_db_type}")
    
    def _initialize_faiss(self):
        """Initialize FAISS vector store"""
        faiss_path = self.vector_db_path / "faiss_index"
        
        if faiss_path.exists():
            logger.info("Loading existing FAISS index")
            return FAISS.load_local(str(faiss_path), self.embeddings, allow_dangerous_deserialization=True)
        else:
            logger.info("Creating new FAISS index")
            # Create empty FAISS store
            return FAISS.from_texts([""], self.embeddings)
    
    def _initialize_chroma(self):
        """Initialize Chroma vector store"""
        chroma_path = self.vector_db_path / "chroma_db"
        
        return Chroma(
            persist_directory=str(chroma_path),
            embedding_function=self.embeddings,
            collection_name="study_documents"
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to vector store"""
        try:
            if self.vector_db_type == "faiss":
                if hasattr(self.vector_store, 'index') and self.vector_store.index.ntotal > 0:
                    # Add to existing FAISS store
                    new_store = FAISS.from_documents(documents, self.embeddings)
                    self.vector_store.merge_from(new_store)
                else:
                    # Create new FAISS store
                    self.vector_store = FAISS.from_documents(documents, self.embeddings)
                
                # Save FAISS index
                faiss_path = self.vector_db_path / "faiss_index"
                self.vector_store.save_local(str(faiss_path))
                
            elif self.vector_db_type == "chroma":
                self.vector_store.add_documents(documents)
            
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents"""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Search for similar documents with scores"""
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} similar documents with scores")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search with score: {e}")
            raise
    
    def get_retriever(self, search_type: str = "similarity", search_kwargs: Dict = None):
        """Get a retriever for the vector store"""
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
    
    def delete_documents(self, ids: List[str]) -> None:
        """Delete documents from vector store"""
        try:
            if self.vector_db_type == "chroma":
                self.vector_store.delete(ids)
                logger.info(f"Deleted {len(ids)} documents from vector store")
            else:
                logger.warning("Document deletion not supported for FAISS")
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            raise
    
    def get_document_count(self) -> int:
        """Get total number of documents in vector store"""
        try:
            if self.vector_db_type == "faiss":
                return self.vector_store.index.ntotal
            elif self.vector_db_type == "chroma":
                return self.vector_store._collection.count()
            return 0
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0

    def get_all_documents(self) -> List[Document]:
        """Get all documents from vector store"""
        try:
            if self.vector_db_type == "faiss":
                # For FAISS, we need to search with a broad query to get all documents
                # This is a workaround since FAISS doesn't have a direct "get all" method
                results = self.vector_store.similarity_search("", k=self.get_document_count())
                return results
            elif self.vector_db_type == "chroma":
                # For Chroma, we can get all documents
                results = self.vector_store.get()
                documents = []
                for i, content in enumerate(results['documents']):
                    doc = Document(
                        page_content=content,
                        metadata=results['metadatas'][i] if results['metadatas'] else {}
                    )
                    documents.append(doc)
                return documents
            return []
        except Exception as e:
            logger.error(f"Error getting all documents: {e}")
            return []
