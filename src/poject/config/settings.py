import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str

    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str 
    S3_BUCKET: str
    S3_PREFIX: str = ""

    # Pinecone
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX: str

    # Local configuration
    VECTOR_DB_IMPL: str = "pinecone"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    LOCAL_DATA_PATH:str = os.path.join(".", "data")

    HOST: str = "0.0.0.0"
    PORT: int = 80
    DEBUG: bool = True

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

# New syntaxe pydantic v2
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
