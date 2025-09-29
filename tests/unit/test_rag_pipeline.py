# test/integration/test_rag_pipeline

import pytest
from src.poject.services.rag_pipeline import RAGPipeline


def test_rag_pipeline(mocker):
    # Arrange
    mock_embeddings = mocker.patch("src.poject.services.rag_pipeline.EmbeddingsService")
    mock_vector_store = mocker.patch("src.poject.services.rag_pipeline.PineconeStore")
    mock_llm = mocker.patch("src.poject.services.rag_pipeline.LLMService")

    # fake embeddings
    mock_embeddings.return_value.embed_texts.return_value = [[0.1, 0.2, 0.3]]

    # fake vector store
    mock_vector_store.return_value.query.return_value = [
        {"metadata": {"text": "Paris is the capital of France"}}
    ]

    # fake LLM
    mock_llm.return_value.chat.return_value = "The capital of France is Paris."

    pipeline = RAGPipeline()

    # Act
    answer = pipeline.ask("What is the capital of France?")

    # Assert
    assert "Paris" in answer
    mock_embeddings.return_value.embed_texts.assert_called_once()
    mock_vector_store.return_value.query.assert_called_once()
    mock_llm.return_value.chat.assert_called_once()
