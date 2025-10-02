# Medical Chatbot - RAG System
An interactive chatbot powered by a **Retrieval-Augmented Generation (RAG)** pipeline, integrating **OpenAI**, **LangChain**, **Pinecone**, **AWS S3** and **Flask**.
The project includes a full pipeline with **automated testing**, **CI/CD via GitHub Actions**, **Docker**, and **deployment on AWS EC2**.

## Features
- Intelligent search via **Pinecone** vectorDB
- Response generation with **OpenAI GPT**
- Data storage with **AWS S3**
- Deployment using **Docker + Amazon ECR**
- **CI/CD GitHub Actions** pipeline (tests → build → automatic deployment)
- Unit, integration, and evaluation tests with **pytest** and **RAGAS**

## Installation
- git clone https://github.com/israaaae/End-to-End-Medical-RAG-Chatbot-Automated-Testing-CI-CD-with-GitHub-Actions-AWS.git
- cd End-to-End-Medical-RAG-Chatbot-Automated-Testing-CI-CD-with-GitHub-Actions-AWS
- poetry install

## Run
- poetry run python -m src.poject.main

## Testing
- poetry run pytest -v

## Project Structure
```
.github/
    └── workflows/
        └── cicd.yaml
data/
    └── medical_book.pdf
scripts/
    └── check.py
src/
    └── poject/
        ├── api/
            ├── app.py
            └── routes.py
        ├── config/
            ├── __init__.py
            └── settings.py
        ├── ingestion_data/
            ├── ingestion.py
            └── storage.py
        ├── models/
            └── chat_request.py
        ├── prompts/
            └── sys_prompt.py
        ├── services/
            ├── embeddings.py
            ├── llm_service.py
            ├── rag_pipeline.py
            └── vector_store.py
        ├── templates/
            └── index.html
        ├── utils/
            └── logger.py
        ├── __init__.py
        ├── main_ingest.py
        └── main.py
tests/
    ├── integration/
        ├── test_rag_pipeline_integ.py
        └── test_routes.py
    ├── ragas_eval/
        └── test_eval_ragas.py
    ├── unit/
        ├── test_embeddings.py
        ├── test_llm_service.py
        ├── test_rag_pipeline.py
        ├── test_storage.py
        └── test_vector_store.py
    └── conftest.py
.gitignore
Dockerfile
LICENSE
poetry.lock
pyproject.toml
pytest.ini
README.md
score.csv
```