from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from src.poject.services.embeddings import EmbeddingsService
from src.poject.services.vector_store import PineconeStore
from src.poject.services.storage import S3Storage
from src.poject.config.settings import settings

bucket = settings.S3_BUCKET
prefix = settings.S3_PREFIX
local = settings.LOCAL_DATA_PATH

def ingest():
    print("Downloading PDFs from S3...")
    s3 = S3Storage()
    s3.download_folder(prefix, local)

    print("Loading local PDFs...")
    loader = DirectoryLoader(local, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    embedder = EmbeddingsService()
    store = PineconeStore()

    print(f"Loaded {len(documents)} documents")
    vectors = []
    for i, doc in enumerate(documents):
        vec = embedder.embed_texts([doc.page_content])[0]
        vectors.append((f"doc_{i}", vec, {"text": doc.page_content}))

    print("Uploading vectors to Pinecone...")
    store.upsert(vectors)
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest()

    
