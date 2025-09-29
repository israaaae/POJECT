from src.poject.ingestion_data.ingestion import IngestionService

def main():
    """Script principal pour l'ingestion"""
    ingestion = IngestionService() 
    ingestion.ingest_from_s3()

if __name__ == "__main__":
    main()