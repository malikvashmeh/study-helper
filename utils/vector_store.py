"""
Vector Store Management
Handles FAISS and Chroma vector databases with Gemini embeddings and enhanced document management
"""

import os
import logging
import json
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path

# Vector database imports
import faiss
import numpy as np
import chromadb
from chromadb.config import Settings

# LangChain imports
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from .local_embeddings import LocalEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS, Chroma

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages vector database operations with enhanced document management"""
    
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
        
        # Document management
        self.metadata_file = self.vector_db_path / "documents_metadata.json"
        self.documents_metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load document metadata from file"""
        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            return {}
    
    def _save_metadata(self):
        """Save document metadata to file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents_metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    
    def _initialize_embeddings(self, embedding_model: str, model_name: str):
        """Initialize embedding model"""
        if embedding_model.lower() == "google":
            return GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        elif embedding_model.lower() == "local":
            return LocalEmbeddings()
        else:
            raise ValueError(f"Unsupported embedding model: {embedding_model}. Supported: google, local")

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
            logger.info("No existing FAISS index found - will create when documents are added")
            return None  # Return None instead of creating empty store
    
    def _initialize_chroma(self):
        """Initialize Chroma vector store"""
        chroma_path = self.vector_db_path / "chroma_db"
        
        return Chroma(
            persist_directory=str(chroma_path),
            embedding_function=self.embeddings,
            collection_name="study_documents"
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to vector store with proper replacement logic"""
        try:
            if not documents:
                logger.warning("No documents to add")
                return
                
            if self.vector_db_type == "faiss":
                # For FAISS, always create fresh store if we don't have one or if explicitly replacing
                if self.vector_store is None:
                    logger.info("Creating new FAISS store")
                    self.vector_store = FAISS.from_documents(documents, self.embeddings)
                else:
                    # Check if we should merge or replace based on existing document count
                    current_count = self.get_document_count()
                    if current_count == 0:
                        # Empty store, create fresh
                        logger.info("Creating fresh FAISS store (was empty)")
                        self.vector_store = FAISS.from_documents(documents, self.embeddings)
                    else:
                        # Merge with existing
                        logger.info(f"Merging {len(documents)} documents with existing {current_count}")
                        new_store = FAISS.from_documents(documents, self.embeddings)
                        try:
                            self.vector_store.merge_from(new_store)
                        except Exception as merge_error:
                            logger.warning(f"Merge failed (likely dimension mismatch): {merge_error}")
                            logger.info("Creating fresh FAISS store due to dimension mismatch")
                            self.vector_store = FAISS.from_documents(documents, self.embeddings)
                
                # Save FAISS index
                faiss_path = self.vector_db_path / "faiss_index"
                self.vector_store.save_local(str(faiss_path))
                
            elif self.vector_db_type == "chroma":
                self.vector_store.add_documents(documents)
            
            # Update metadata tracking
            self._update_documents_metadata(documents)
            self._save_metadata()
            
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def _update_documents_metadata(self, documents: List[Document]):
        """Update internal metadata tracking"""
        for doc in documents:
            if 'document_id' in doc.metadata:
                doc_id = doc.metadata['document_id']
                self.documents_metadata[doc_id] = {
                    'filename': doc.metadata.get('filename', 'unknown'),
                    'content_hash': doc.metadata.get('content_hash', ''),
                    'processing_timestamp': doc.metadata.get('processing_timestamp', ''),
                    'chunk_count': doc.metadata.get('total_chunks', 1),
                    'file_type': doc.metadata.get('file_type', ''),
                    'file_size': doc.metadata.get('file_size', 0)
                }
    
    def clear_all_documents(self) -> bool:
        """Clear all documents from vector store and completely reset memory"""
        try:
            logger.info("Completely clearing all documents from vector store")
            
            if self.vector_db_type == "faiss":
                # Remove FAISS index files completely
                faiss_path = self.vector_db_path / "faiss_index"
                if faiss_path.exists():
                    shutil.rmtree(faiss_path)
                    logger.info("Removed FAISS index files")
                
                # Set vector store to None (no empty placeholder)
                self.vector_store = None
                logger.info("Reset FAISS vector store to empty state")
                
            elif self.vector_db_type == "chroma":
                # For Chroma, delete and recreate collection
                try:
                    self.vector_store.delete_collection()
                except:
                    pass  # Collection might not exist
                
                # Reinitialize Chroma
                self.vector_store = self._initialize_chroma()
            
            # Clear metadata completely
            self.documents_metadata.clear()
            self._save_metadata()
            
            logger.info("Successfully cleared all documents and reset memory completely")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing documents: {e}")
            return False
    
    def replace_all_documents(self, documents: List[Document]) -> bool:
        """Replace all existing documents with new ones (clear + add)"""
        try:
            logger.info(f"Replacing all documents with {len(documents)} new documents")
            
            # Clear everything first
            if not self.clear_all_documents():
                return False
            
            # Add new documents
            if documents:
                self.add_documents(documents)
            
            logger.info("Successfully replaced all documents")
            return True
            
        except Exception as e:
            logger.error(f"Error replacing documents: {e}")
            return False
    
    def get_documents_by_metadata(self, filter_criteria: Dict[str, Any]) -> List[Document]:
        """Get documents that match specific metadata criteria"""
        try:
            all_docs = self.get_all_documents()
            filtered_docs = []
            
            for doc in all_docs:
                match = True
                for key, value in filter_criteria.items():
                    if key not in doc.metadata or doc.metadata[key] != value:
                        match = False
                        break
                if match:
                    filtered_docs.append(doc)
            
            logger.info(f"Found {len(filtered_docs)} documents matching criteria")
            return filtered_docs
            
        except Exception as e:
            logger.error(f"Error filtering documents: {e}")
            return []
    
    def remove_documents_by_criteria(self, filter_criteria: Dict[str, Any]) -> int:
        """Remove documents that match specific criteria (Chroma only)"""
        try:
            if self.vector_db_type != "chroma":
                logger.warning("Document removal by criteria only supported for Chroma")
                return 0
            
            # Get matching documents
            matching_docs = self.get_documents_by_metadata(filter_criteria)
            
            if not matching_docs:
                logger.info("No documents match removal criteria")
                return 0
            
            # Extract IDs for deletion (this is a simplified approach)
            # In practice, you'd need proper ID tracking
            logger.warning("Document removal by criteria requires proper ID tracking implementation")
            return 0
            
        except Exception as e:
            logger.error(f"Error removing documents: {e}")
            return 0
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """Create backup of current vector store"""
        try:
            if backup_name is None:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_path = self.vector_db_path / "backups" / backup_name
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Copy vector store files
            if self.vector_db_type == "faiss":
                faiss_path = self.vector_db_path / "faiss_index"
                if faiss_path.exists():
                    shutil.copytree(faiss_path, backup_path / "faiss_index", dirs_exist_ok=True)
            elif self.vector_db_type == "chroma":
                chroma_path = self.vector_db_path / "chroma_db"
                if chroma_path.exists():
                    shutil.copytree(chroma_path, backup_path / "chroma_db", dirs_exist_ok=True)
            
            # Copy metadata
            if self.metadata_file.exists():
                shutil.copy2(self.metadata_file, backup_path / "documents_metadata.json")
            
            logger.info(f"Created backup: {backup_name}")
            return backup_name
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return ""
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore vector store from backup"""
        try:
            backup_path = self.vector_db_path / "backups" / backup_name
            
            if not backup_path.exists():
                logger.error(f"Backup {backup_name} not found")
                return False
            
            # Clear current data
            self.clear_all_documents()
            
            # Restore vector store
            if self.vector_db_type == "faiss":
                backup_faiss = backup_path / "faiss_index"
                if backup_faiss.exists():
                    target_path = self.vector_db_path / "faiss_index"
                    shutil.copytree(backup_faiss, target_path, dirs_exist_ok=True)
                    # Reload FAISS store
                    self.vector_store = self._initialize_faiss()
                    
            elif self.vector_db_type == "chroma":
                backup_chroma = backup_path / "chroma_db"
                if backup_chroma.exists():
                    target_path = self.vector_db_path / "chroma_db"
                    shutil.copytree(backup_chroma, target_path, dirs_exist_ok=True)
                    # Reload Chroma store
                    self.vector_store = self._initialize_chroma()
            
            # Restore metadata
            backup_metadata = backup_path / "documents_metadata.json"
            if backup_metadata.exists():
                shutil.copy2(backup_metadata, self.metadata_file)
                self.documents_metadata = self._load_metadata()
            
            logger.info(f"Restored backup: {backup_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def get_store_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the vector store"""
        try:
            stats = {
                'vector_db_type': self.vector_db_type,
                'total_documents': self.get_document_count(),
                'metadata_tracked_docs': len(self.documents_metadata),
                'unique_files': len(set(doc['filename'] for doc in self.documents_metadata.values())),
                'storage_path': str(self.vector_db_path),
                'last_update': datetime.now().isoformat()
            }
            
            # File type breakdown
            file_types = {}
            for doc_meta in self.documents_metadata.values():
                file_type = doc_meta.get('file_type', 'unknown')
                file_types[file_type] = file_types.get(file_type, 0) + 1
            stats['file_types'] = file_types
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting store stats: {e}")
            return {'error': str(e)}
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents"""
        try:
            if self.vector_store is None:
                logger.warning("No vector store available for search")
                return []
            
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
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
                if self.vector_store is None:
                    return 0
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
                if self.vector_store is None:
                    return []
                
                # For FAISS, we need to search with a broad query to get all documents
                document_count = self.get_document_count()
                if document_count == 0:
                    return []
                
                # Use a broad search to get all documents
                results = self.vector_store.similarity_search("", k=document_count)
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
