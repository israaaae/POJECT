# tests/unit/test_vector_store_aaa.py
import pytest
from unittest.mock import patch, Mock
from src.poject.services.vector_store import PineconeStore

@pytest.mark.unit
def test_pinecone_store(mock_pinecone):
    """PineconeStore:upsert & query"""
    mock_pc_instance, mock_index = mock_pinecone
    store = PineconeStore()
    vectors = [("id1", [0.1, 0.2, 0.3], {"meta": "data"})]
    store.fct_upsert(vectors)
    mock_index.upsert.assert_called_once_with(vectors=vectors)
    mock_index.query.return_value = {
        "matches": [{"id": "id1", "score": 0.9, "metadata": {"meta": "data"}}]
    }
    vector = [0.1, 0.2, 0.3]
    top_k = 1
    results = store.fct_query(vector, top_k)
    mock_index.query.assert_called_once_with(vector=vector, top_k=top_k, include_metadata=True)
    assert results == [{"id": "id1", "score": 0.9, "metadata": {"meta": "data"}}]
