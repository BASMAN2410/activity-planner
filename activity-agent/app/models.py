from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class MCPMessage(BaseModel):
    message_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    source: Optional[str] = None

class MCPResponse(BaseModel):
    message_id: str
    response: str
    status: str
    activities: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    title: str
    description: str
    url: Optional[str] = None
    score: float 