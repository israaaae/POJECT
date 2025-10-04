# tests/integration/test_rag_pipeline_integ.py
import pytest
from src.poject.services.rag_pipeline import RAGPipeline

pytestmark = pytest.mark.integration

def test_rag_pipeline_integ(mock_embeddings, mock_pinecone, mock_llm):
    """Integration test with medical questions"""
    mock_pc_instance, mock_index = mock_pinecone
    pipeline = RAGPipeline()
    mock_embeddings.embed_texts.return_value = [[0.1, 0.2, 0.3]]
    mock_index.query.return_value = {
        "matches": [
            {
                "metadata": {
                    "text": "L'hypertension artérielle se traite par des inhibiteurs de l'ECA, des bêta-bloquants, et des mesures hygiéno-diététiques.",
                    "source": "Guide de cardiologie"
                }
            },
            {
                "metadata": {
                    "text": "La réduction du sel et l'activité physique régulière sont recommandées.",
                    "source": "Recommandations HAS"
                }
            }
        ]
    }
    
    mock_llm.chat.return_value = "L'hypertension peut être traitée avec des médicaments comme les inhibiteurs de l'ECA et des changements de mode de vie comme la réduction du sel."
    # Act
    answer = pipeline.ask("Traitement pour l'hypertension ?")
    # Assert
    assert "hypertension" in answer.lower()
    assert any(keyword in answer.lower() for keyword in ["traitement", "médicament", "inhibiteurs", "sel"])

    mock_embeddings.embed_texts.assert_called_once_with(["Traitement pour l'hypertension ?"])
    mock_index.query.assert_called_once_with(vector=[0.1, 0.2, 0.3], top_k=3, include_metadata=True)
    mock_llm.chat.assert_called_once()
