# tests/unit/test_storage.py
import pytest
from src.poject.ingestion_data.storage import S3Storage

def test_s3_storage_downloads_medical_pdf(mocker, tmp_path):
    """Test ESSENTIEL - Téléchargement d'un PDF médical"""
    # Arrange
    mock_boto3 = mocker.patch("src.poject.ingestion_data.storage.boto3.client")
    mock_s3 = mock_boto3.return_value
    
    storage = S3Storage()
    medical_pdf_path = tmp_path / "data" / "Medical_book.pdf"

    # Act
    storage.download_file("Medical_book.pdf", str(medical_pdf_path))

    # Assert
    # 1. Vérifier que le dossier est créé
    assert medical_pdf_path.parent.exists()
    
    # 2. Vérifier l'appel S3 avec les bons paramètres
    mock_s3.download_file.assert_called_once_with(
        storage.bucket,           # Bucket depuis settings
        "Medical_book.pdf",       # Clé S3 exacte
        str(medical_pdf_path)     # Destination exacte
    )
    
    # 3. Vérifier que c'est bien un appel de téléchargement
    assert mock_s3.download_file.called