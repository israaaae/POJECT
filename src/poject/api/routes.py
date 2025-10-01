# src/poject/api/routes.py
from flask import Blueprint, request, jsonify
from ..utils.logger import logger
from pydantic import ValidationError
from ..models.chat_request import ChatRequest
bp = Blueprint("api", __name__)
from src.poject.services.rag_pipeline import RAGPipeline

pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        pipeline = RAGPipeline()
    return pipeline

@bp.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}

@bp.post("/chat")
def chat():
    try:
        payload = request.get_json(force=True)
        try:
            req = ChatRequest(**payload)
        except ValidationError as ve:
            return {"success": False, "error": ve.errors()}, 400

        logger.info(f"Received question: '{req.question}', top_k={req.top_k}")
        rag_pipeline = get_pipeline()
        answer = rag_pipeline.ask(req.question, top_k=req.top_k)

        return {"success": True, "answer": answer, "error": None}, 200 
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
