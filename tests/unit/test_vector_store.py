# tests/unit/test_vector_store.py

import pytest
from src.poject.services.vector_store import PineconeStore


def test_pinecone_upsert_and_query(mocker):
    # Arrange
    mock_pinecone = mocker.patch("src.poject.services.vector_store.Pinecone")
    mock_pc = mock_pinecone.return_value
    mock_index = mock_pc.Index.return_value

    store = PineconeStore()

    # Act
    vectors = [("id1", [0.1, 0.2, 0.3], {"text": "sample"})]
    store.fct_upsert(vectors)
    store.fct_query([0.1, 0.2, 0.3], top_k=3)

    # Assert
    mock_index.upsert.assert_called_once_with(vectors=vectors)
    mock_index.query.assert_called_once_with(vector=[0.1, 0.2, 0.3], top_k=3, include_metadata=True)

