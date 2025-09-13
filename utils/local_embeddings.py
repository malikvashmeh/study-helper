# utils/local_embeddings.py
"""
LangChain-compatible wrapper for local embeddings
"""
import os
from typing import List
import numpy as np
from langchain.schema.embeddings import Embeddings
from .embeddings import EmbeddingService

class LocalEmbeddings(Embeddings):
    """LangChain-compatible wrapper for local embeddings"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        vectors = self.embedding_service.embed(texts)
        return [vector.tolist() for vector in vectors]
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        vectors = self.embedding_service.embed([text])
        return vectors[0].tolist()
