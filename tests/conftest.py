# tests/conftest.py
import pytest
import numpy as np
from unittest.mock import Mock, patch
from langchain.docstore.document import Document


# -------------------
# Flask fixtures
# -------------------
@pytest.fixture
def app():
    """Application Flask pour les tests"""
    from src.poject.api.app import create_app
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()


# -------------------
# Mocks externes
# -------------------
@pytest.fixture(autouse=True)
def mock_sentence_transformers(monkeypatch):
    """Mock global pour SentenceTransformer (évite de charger un vrai modèle)"""
    fake_model = Mock()
    fake_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
    # Toute tentative d’instancier SentenceTransformer() dans le code test sera remplacée par fake_model
    monkeypatch.setattr("sentence_transformers.SentenceTransformer",lambda *args, **kwargs: fake_model)
    return fake_model 

@pytest.fixture
def mock_embeddings():
    """Mock pour EmbeddingsService"""
    with patch("src.poject.services.embeddings.EmbeddingsService") as mock_emb:
        mock_emb_instance = Mock()
        mock_emb_instance.embed_texts.return_value = [[0.1] * 384, [0.2] * 384]
        mock_emb.return_value = mock_emb_instance
        yield mock_emb_instance


@pytest.fixture
def mock_pinecone():
    """Mock pour Pinecone"""
    with patch("src.poject.services.vector_store.pinecone") as mock_pc:
        mock_index = Mock()
        mock_index.upsert.return_value = None
        mock_index.query.return_value = {"matches": []}

        mock_pc.init.return_value = None
        mock_pc.list_indexes.return_value = ["test-index"]
        mock_pc.Index.return_value = mock_index
        mock_pc.create_index.return_value = None

        yield mock_pc, mock_index


@pytest.fixture
def mock_s3():
    """Mock pour le client S3"""
    with patch("src.poject.ingestion_data.storage.boto3.client") as mock_client:  # ✅ corrigé (avant ingestion_data)
        mock_s3 = Mock()
        mock_s3.list_objects.return_value = {"Contents": []}
        mock_s3.download_file.return_value = None
        mock_client.return_value = mock_s3
        yield mock_s3


@pytest.fixture
def mock_llm():
    """Mock pour le service LLM"""
    with patch("src.poject.services.llm_service.LLMService") as mock_llm_class:
        mock_llm_instance = Mock()
        mock_llm_instance.chat.return_value = "Réponse simulée du LLM"
        mock_llm_class.return_value = mock_llm_instance
        yield mock_llm_instance


# -------------------
# Données exemples
# -------------------
@pytest.fixture
def sample_documents():
    return [
        Document(
            page_content="Les maladies cardiovasculaires sont la première cause de mortalité mondiale.",
            metadata={"source": "medical_guide.pdf", "page": 1, "chunk_id": "doc_1_chunk_1"},
        ),
        Document(
            page_content="Le diabète se caractérise par une hyperglycémie chronique.",
            metadata={"source": "endocrinology.pdf", "page": 15, "chunk_id": "doc_2_chunk_1"},
        ),
    ]


@pytest.fixture
def sample_embeddings():
    """Embeddings simulés pour les tests"""
    return [[0.1] * 384, [0.2] * 384]
