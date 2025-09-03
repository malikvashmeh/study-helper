"""
Document Processing Utilities
Handles PDF, text, and other document formats
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path

# Document processing imports
import PyPDF2
from docx import Document
import tiktoken

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document as LangChainDocument

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document loading and text extraction"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            raise
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX {file_path}: {e}")
            raise
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Error extracting text from TXT {file_path}: {e}")
            raise
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[LangChainDocument]:
        """Split text into chunks and return as LangChain Documents"""
        if metadata is None:
            metadata = {}
        
        # Split the text
        chunks = self.text_splitter.split_text(text)
        
        # Convert to LangChain Documents
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = metadata.copy()
            doc_metadata.update({
                'chunk_id': i,
                'total_chunks': len(chunks)
            })
            documents.append(LangChainDocument(
                page_content=chunk,
                metadata=doc_metadata
            ))
        
        return documents
    
    def process_document(self, file_path: str) -> List[LangChainDocument]:
        """Complete document processing pipeline"""
        try:
            # Extract text
            text = self.extract_text(file_path)
            
            # Create metadata
            file_name = Path(file_path).name
            metadata = {
                'source': file_path,
                'filename': file_name,
                'file_type': Path(file_path).suffix.lower()
            }
            
            # Chunk the text
            documents = self.chunk_text(text, metadata)
            
            logger.info(f"Processed {file_name}: {len(documents)} chunks created")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            raise
    
    def get_token_count(self, text: str) -> int:
        """Get approximate token count for text"""
        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except:
            # Fallback: rough estimate (4 characters per token)
            return len(text) // 4
