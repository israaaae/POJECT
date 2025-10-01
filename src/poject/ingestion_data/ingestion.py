# src/poject/services/ingestion.py
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..services.embeddings import EmbeddingsService
from ..services.vector_store import PineconeStore
from .storage import S3Storage
from ..config.settings import settings
from ..utils.logger import logger

s3_prefix = settings.S3_PREFIX
local_folder = settings.LOCAL_DATA_PATH

class IngestionService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.embedding = EmbeddingsService()
        self.store = PineconeStore()
        self.s3 = S3Storage()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        logger.info("IngestionService initialized")

    def ingest_from_s3(self, s3_prefix: str = "", local_folder: str = settings.LOCAL_DATA_PATH):
        """Downloading from s3"""
        logger.info("Downloading PDFs from S3...")
        self.s3.download_folder(s3_prefix, local_folder)
        self.ingest_from_local(local_folder)

    def ingest_from_local(self, folder: str):
        """ingesting from local Pinecone"""
        logger.info("Loading local PDFs...")
        loader = DirectoryLoader(folder, glob="*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        logger.info("Loaded %d raw documents", len(docs))
        # splitting to chunks
        chunks = self.splitter.split_documents(docs)
        logger.info("Produced %d chunks", len(chunks))
        # Embedding
        texts = [d.page_content for d in chunks]
        logger.info("Embedding documents...")
        embeddings = self.embedding.embed_texts(texts)
        # Preparing vectors
        vectors = []
        for i, (vec, doc) in enumerate(zip(embeddings, chunks)):
            meta = {
                "text": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "chunk_id": f"chunk_{i}"
            }
            vectors.append((f"doc_{i}", vec, meta))
        # Upsert to Pinecone
        logger.info("Uploading %d vectors to Pinecone...", len(vectors))
        self.store.fct_upsert(vectors) 
        
        logger.info("Ingestion complete! %d vectors upserted", len(vectors))
        return len(vectors)