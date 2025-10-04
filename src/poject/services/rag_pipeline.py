# src/services/rag_pipeline.py
from typing import List
from ..services.embeddings import EmbeddingsService
from ..services.vector_store import PineconeStore
from ..services.llm_service import LLMService
from ..utils.logger import logger

class RAGPipeline:
    def __init__(self):
        self.embedding = EmbeddingsService()
        self.store = PineconeStore()
        self.llm = LLMService()
        logger.info("RAGPipeline initialized")

    def ask(self, question: str, top_k: int = 3) -> str:
        q_emb = self.embedding.embed_texts([question])[0]
        matches = self.store.fct_query(q_emb, top_k=top_k)
        context_parts: List[str] = []
        for m in matches:
            meta = m.get("metadata", {})
            text = meta.get("text") or meta.get("content") or meta.get("source", "")
            context_parts.append(f"Source: {meta.get('source', '')}\n{text}\n") 
        context = "\n".join(context_parts)[:3000]  
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer succinctly and medically accurate."
        return self.llm.chat(prompt)
