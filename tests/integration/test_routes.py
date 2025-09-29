# tests/integration/test_routes.py

import pytest

def test_health_endpoint_returns_ok(client):
    """Test que l'endpoint health fonctionne"""
    # ARRANGE - client fixture
    
    # ACT
    response = client.get('/api/health')

    # ASSERT
    assert response.status_code == 200
    assert b'ok' in response.data

def test_chat_endpoint_answers_questions(client, mocker):
    # ARRANGE
    mock_pipeline = mocker.patch("src.poject.api.routes.get_pipeline")
    mock_pipeline.return_value.ask.return_value = "Réponse à votre question médicale"

    # ACT
    response = client.post('/api/chat', json={
        "question": "Traitement pour l'hypertension ?"
    })
    data = response.get_json()  # décode proprement le JSON

    # ASSERT
    assert response.status_code == 200
    assert "Réponse" in data["answer"]




# on teste réellement que la route fonctionne et que le template est chargé
def test_index_endpoint_renders_template(client):
    response = client.get("/")
    assert response.status_code == 200
    # Vérifie juste que le contenu ressemble à HTML
    assert b"<html" in response.data
    assert b"</html>" in response.data
