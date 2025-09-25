# src/models/chat_request.py
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Schema for incoming chat/query requests."""
    question: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(3, gt=0, description="Number of relevant docs to retrieve")
