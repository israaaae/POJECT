# src/services/embeddings.py
from typing import List, Iterable
from sentence_transformers import SentenceTransformer
from ..config.settings import settings
from ..utils.logger import logger

class EmbeddingsService:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        logger.info("Loading sentence-transformers model: %s", self.model_name)
        self.model = SentenceTransformer(self.model_name)

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        """Embed a list/iterable of texts -> list of vectors."""
        texts = list(texts)
        vectors = self.model.encode(texts, show_progress_bar=False)
        return vectors.tolist()
