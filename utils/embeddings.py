# utils/embeddings.py
import os
import hashlib
import pickle
from typing import List
import numpy as np

# Local embedding model
from sentence_transformers import SentenceTransformer

# Constants come from environment with sensible defaults
CACHE_PATH = os.getenv("EMBEDDINGS_CACHE_PATH", "data/embeddings_cache.pkl")
HF_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()

class EmbeddingService:
    """
    Simple embedding service with a persistent disk cache.
    Default provider is local SentenceTransformer.
    Returns list[np.ndarray(dtype=float32)] for given texts.
    """

    def __init__(self):
        self.cache = self._load_cache()
        self.hf_model = None
        if PROVIDER == "local":
            self._init_hf()

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _load_cache(self):
        try:
            if os.path.exists(CACHE_PATH):
                with open(CACHE_PATH, "rb") as f:
                    return pickle.load(f)
        except Exception:
            # If cache is corrupt, ignore and start fresh
            pass
        return {}

    def _save_cache(self):
        os.makedirs(os.path.dirname(CACHE_PATH) or ".", exist_ok=True)
        with open(CACHE_PATH, "wb") as f:
            pickle.dump(self.cache, f)

    def _init_hf(self):
        # Lazy load model
        if self.hf_model is None:
            self.hf_model = SentenceTransformer(HF_MODEL)

    def embed(self, texts: List[str]) -> List[np.ndarray]:
        """
        Embed a list of texts. Uses cache for previously seen texts. New texts are embedded
        with the local HF model and added to cache. Returns numpy.float32 vectors.
        """
        results = []
        to_embed = []
        missing_indexes = []

        for i, t in enumerate(texts):
            h = self._hash(t)
            if h in self.cache:
                vec = np.array(self.cache[h], dtype=np.float32)
                results.append(vec)
            else:
                results.append(None)
                to_embed.append(t)
                missing_indexes.append(i)

        if to_embed:
            if PROVIDER != "local":
                # If you later want Gemini fallback, insert call here.
                # For now, do local embeddings only to avoid Gemini quota.
                raise RuntimeError("Non-local providers are not enabled. Set EMBEDDING_PROVIDER=local")

            self._init_hf()
            vecs = self.hf_model.encode(to_embed, convert_to_numpy=True, show_progress_bar=False)
            if isinstance(vecs, np.ndarray) is False:
                vecs = np.array(vecs)

            for idx, vec in zip(missing_indexes, vecs):
                vec = np.array(vec, dtype=np.float32)
                results[idx] = vec
                self.cache[self._hash(texts[idx])] = vec.tolist()

            self._save_cache()

        return results
