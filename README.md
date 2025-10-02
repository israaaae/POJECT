# Medical Chatbot - RAG System
An interactive chatbot powered by a **Retrieval-Augmented Generation (RAG)** pipeline, integrating **OpenAI**, **LangChain**, **Pinecone**, **AWS S3**, **Flask**.
The project includes a full pipeline with **automated testing**, **CI/CD via GitHub Actions**, **Docker**, and **deployment on AWS EC2**.

## Features
- Intelligent search via **Pinecone** vectorDB
- Response generation with **OpenAI GPT**
- Data storage with **AWS S3**
- Deployment using **Docker + Amazon ECR**
- **CI/CD GitHub Actions** pipeline (tests → build → automatic deployment)
- Unit, integration, and evaluation tests with **pytest** and **RAGAS**

## Installation
1) git clone https://github.com/israaaae/End-to-End-Medical-RAG-Chatbot-Automated-Testing-CI-CD-with-GitHub-Actions-AWS.git
2) cd End-to-End-Medical-RAG-Chatbot-Automated-Testing-CI-CD-with-GitHub-Actions-AWS
3) poetry install

## Run
poetry run python -m src.poject.main

## Testing
poetry run pytest -v