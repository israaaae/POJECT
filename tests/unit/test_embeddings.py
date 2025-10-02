# tests/unit/test_embeddings.py
import pytest
import numpy as np
from src.poject.services.embeddings import EmbeddingsService
@pytest.mark.unit
def test_embeddings(mocker):
    # Arrange
    mock_model = mocker.patch("src.poject.services.embeddings.SentenceTransformer")
    mock_numpy_array = np.array([[0.1, 0.2, 0.3]])
    mock_model.return_value.encode.return_value = mock_numpy_array

    service = EmbeddingsService()

    # Act
    result = service.embed_texts(["hello world"])

    # Assert
    assert isinstance(result, list)
    assert result[0] == [0.1, 0.2, 0.3]
    mock_model.return_value.encode.assert_called_once_with(["hello world"], show_progress_bar=True)