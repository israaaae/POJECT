# tests/unit/test_storage.py
import pytest
from src.poject.ingestion_data.storage import S3Storage

@pytest.mark.unit
def test_s3_storage_downloads_medical_pdf(mocker, tmp_path):
    # Arrange
    mock_boto3 = mocker.patch("src.poject.ingestion_data.storage.boto3.client")
    mock_s3 = mock_boto3.return_value

    storage = S3Storage()
    medical_pdf_path = tmp_path / "data" / "Medical_book.pdf"

    # Act
    storage.download_file("Medical_book.pdf", str(medical_pdf_path))

    # Assert
    assert medical_pdf_path.parent.exists()
    
    mock_s3.download_file.assert_called_once_with(
        storage.bucket,     
        "Medical_book.pdf",     
        str(medical_pdf_path)    
    )

    assert mock_s3.download_file.called