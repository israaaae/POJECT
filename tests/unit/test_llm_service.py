# tests/unit/test_llm_service.py
import pytest
from src.poject.services.llm_service import LLMService

def test_llm_service_chat_returns_text(mocker):
    """Test que chat() retourne une réponse textuelle"""
    # ARRANGE
    mock_client = mocker.patch("src.poject.services.llm_service.OpenAI")
    
    # Configurer le mock pour la NOUVELLE API OpenAI
    mock_response = mocker.Mock()
    mock_message = mocker.Mock(content="Réponse simulée de l'IA médicale")
    mock_choice = mocker.Mock(message=mock_message)
    mock_response.choices = [mock_choice]
    
    mock_client.return_value.chat.completions.create.return_value = mock_response

    llm = LLMService()

    # ACT
    result = llm.chat("Quels sont les symptômes du diabète ?")

    # ASSERT
    assert result == "Réponse simulée de l'IA médicale"
    mock_client.return_value.chat.completions.create.assert_called_once()

