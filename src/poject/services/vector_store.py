# src/services/vector_store.py
from typing import List, Sequence, Tuple
from ..config.settings import settings
from ..utils.logger import logger

_HAS_PINECONE = True
try:
    from pinecone import Pinecone
except Exception:
    _HAS_PINECONE = False


class PineconeStore:
    def __init__(self):
        if not _HAS_PINECONE:
            raise RuntimeError("pinecone client not installed")
        self.index_name = settings.PINECONE_INDEX
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY,environment=settings.PINECONE_ENVIRONMENT)
        logger.info("Pinecone client initialized, index=%s", self.index_name)
        if self.index_name not in self.pc.list_indexes().names():
            logger.warning(
                "Index %s not found in Pinecone. Create it in Pinecone console beforehand.",
                self.index_name
            )
        self.index = self.pc.Index(self.index_name)  # Index: I en majuscule

    def fct_upsert(self, vectors: Sequence[Tuple[str, List[float], dict]]) -> None:
        """Upsert list of (id, vector, metadata)"""
        self.index.upsert(vectors=vectors)

    def fct_query(self, vector: List[float], top_k: int):
        """Query the index"""
        resp = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
        matches = resp.get("matches", [])
        return matches

