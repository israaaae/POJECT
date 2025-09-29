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
        # embed question
        q_emb = self.embedding.embed_texts([question])[0]
        matches = self.store.fct_query(q_emb, top_k=top_k)
        # build context from metadata (note: depends how you stored metadata)
        context_parts: List[str] = []
        for m in matches:
            meta = m.get("metadata", {})
            text = meta.get("text") or meta.get("content") or meta.get("source", "")
            context_parts.append(f"Source: {meta.get('source', '')}\n{text}\n") # context_parts contient le partie 'text' des 3 matches returnés
        context = "\n".join(context_parts)[:3000]  # limit prompt size
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer succinctly and medically accurate."
        return self.llm.chat(prompt)


# LLM recoit une prompt de type :
# Context:
# Source: article1.pdf
# La grippe est une infection virale courante.
# ---
# Source: article2.pdf
# Les symptômes incluent fièvre, toux et fatigue.
# ---

# Question: Quels sont les symptômes de la grippe ?
# Answer succinctly and medically accurate.