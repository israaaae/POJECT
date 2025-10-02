# scripts/health_check.py
from src.poject.services.vector_store import PineconeStore
from src.poject.services.llm_service import LLMService
from src.poject.utils.logger import logger

def run_checks():
    ok = True
    try:
        PineconeStore()
        logger.info("Pinecone client OK")
    except Exception as e:
        logger.exception("Pinecone error: %s", e)
        ok = False

    try:
        LLMService()
        logger.info("LLM OK")
    except Exception as e:
        logger.exception("LLM error: %s", e)
        ok = False

    return ok

if __name__ == "__main__":
    if not run_checks():
        raise SystemExit(1)
