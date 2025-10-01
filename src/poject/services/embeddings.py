# src/services/embeddings.py
from typing import List, Iterable
from sentence_transformers import SentenceTransformer
from ..config.settings import settings
from ..utils.logger import logger

class EmbeddingsService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        logger.info("Loading sentence-transformers model: %s", self.model_name)
        self.model = SentenceTransformer(self.model_name)

    def embed_texts(self, texts: Iterable[str]) -> List[List[float]]:
        """Embed a list of texts to list of vectors."""
        texts = list(texts)
        vectors = self.model.encode(texts, show_progress_bar=True)
        return vectors.tolist()
