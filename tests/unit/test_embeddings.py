# tests/unit/test_embeddings.py
import pytest
import numpy as np
from src.poject.services.embeddings import EmbeddingsService

def test_embeddings_service_returns_vectors(mocker):
    """Test ESSENTIEL que embed_texts() fonctionne"""
    # Arrange
    mock_model = mocker.patch("src.poject.services.embeddings.SentenceTransformer")
    mock_numpy_array = np.array([[0.1, 0.2, 0.3]])  # 1 texte, 3 dimensions
    mock_model.return_value.encode.return_value = mock_numpy_array

    service = EmbeddingsService()

    # Act
    result = service.embed_texts(["hello world"])

    # Assert
    assert isinstance(result, list)
    assert result[0] == [0.1, 0.2, 0.3]
    mock_model.return_value.encode.assert_called_once_with(["hello world"], show_progress_bar=False)