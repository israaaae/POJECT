# src/services/rag_pipeline.py
from typing import List
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..services.embeddings import EmbeddingsService
from ..services.vector_store import PineconeStore
from ..services.llm_service import LLMService
from ..utils.logger import logger

class RAGPipeline:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.embedding = EmbeddingsService()
        self.store = PineconeStore()
        self.llm = LLMService()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        logger.info("RAGPipeline initialized")

    def ingest_from_local(self, folder: str):
        """Load PDFs from local folder, chunk, embed and upsert"""
        loader = DirectoryLoader(folder, glob="*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        logger.info("Loaded %d raw documents", len(docs))
        chunks = self.splitter.split_documents(docs)
        logger.info("Produced %d chunks", len(chunks))
        texts = [d.page_content for d in chunks]
        embeddings = self.embedding.embed_texts(texts)
        vectors = []
        for i, (vec, doc) in enumerate(zip(embeddings, chunks)):
            meta = {"source": getattr(doc, "metadata", {}).get("source", None)}
            vectors.append((f"doc-{i}", vec, meta))
        self.store.upsert(vectors)
        logger.info("Upserted %d vectors", len(vectors))

    def ingest_from_s3(self, s3_prefix: str, local_folder: str, s3_client):
        """Download PDFs from S3 and ingest locally."""
        s3_client.download_folder(s3_prefix, local_folder)
        self.ingest_from_local(local_folder)

    def ask(self, question: str, top_k: int = 4) -> str:
        # embed question
        q_emb = self.embedding.embed_texts([question])[0]
        matches = self.store.query(q_emb, top_k=top_k)
        # build context from metadata (note: depends how you stored metadata)
        context_parts: List[str] = []
        for m in matches:
            meta = m.get("metadata", {})
            text = meta.get("text") or meta.get("content") or meta.get("source", "")
            context_parts.append(f"Source: {meta.get('source', '')}\n{text}\n---\n")
        context = "\n".join(context_parts)[:3000]  # limit prompt size
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer succinctly and medically accurate."
        return self.llm.chat(prompt)
