from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MCPMessage(BaseModel):
    """
    Model for a received MCP message.
    """
    message_id: str = Field(..., description="Unique identifier for the message")
    content: str = Field(..., description="The text content of the message")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata about the message")
    source: Optional[str] = Field(default=None, description="Source of the message (e.g., Slack, Twitter)")

class MCPResponse(BaseModel):
    """
    Standard MCP response.
    """
    message_id: str = Field(..., description="Unique identifier for the response")
    response: str = Field(..., description="Generated response text")
    status: str = Field(..., description="Processing status (e.g., success, failed)")
    activities: Optional[List[Dict[str, Any]]] = Field(default=None, description="List of planned activities (if any)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class SearchResult(BaseModel):
    """
    Model for search result entries.
    """
    title: str = Field(..., description="Title of the search result")
    description: str = Field(..., description="Short description of the result")
    url: Optional[str] = Field(default=None, description="URL to the full resource")
    score: float = Field(..., description="Relevance score")

class SummarizationRequest(BaseModel):
    """
    Model for text summarization requests.
    """
    text: str = Field(..., description="The text to be summarized")
    max_length: int = Field(150, description="Maximum length of the summary in words")
    min_length: int = Field(50, description="Minimum length of the summary in words")
    format: str = Field("paragraph", description="Format of the summary (paragraph, bullets, etc.)")

class SummarizationResponse(BaseModel):
    """
    Model for summarization responses.
    """
    summary: str = Field(..., description="Generated summary text")
    original_length: int = Field(..., description="Original length of the input text")
    summary_length: int = Field(..., description="Length of the generated summary")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Optional error details")

class QuestionRequest(BaseModel):
    """
    Model for question answering requests.
    """
    question: str = Field(..., description="The question to be answered")
    context: Optional[str] = Field(None, description="Optional context to help answer the question")
    format: str = Field("detailed", description="Format of the answer (detailed or concise)")

class QuestionResponse(BaseModel):
    """
    Model for question answering responses.
    """
    status: str = Field(..., description="Status of the request")
    answer: str = Field(..., description="Generated answer")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata about the response")
