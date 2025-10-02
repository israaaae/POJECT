# tests/integration/test_routes.py

import pytest

pytestmark = pytest.mark.integration
def test_chat_endpoint_answers_questions(client, mocker):
    # ARRANGE
    mock_pipeline = mocker.patch("src.poject.api.routes.get_pipeline")
    mock_pipeline.return_value.ask.return_value = "Réponse à votre question médicale"
    
    # ACT
    response = client.post('/api/chat', json={
        "question": "Traitement pour l'hypertension ?"
    })
    data = response.get_json()
    
    # ASSERT
    assert response.status_code == 200
    assert "Réponse" in data["answer"]
    mock_pipeline.return_value.ask.assert_called_once_with("Traitement pour l'hypertension ?", top_k=3)

def test_index_endpoint(client):
    # ACT
    response = client.get("/")
    
    # ASSERT
    assert response.status_code == 200
    assert b"<html>" in response.data

