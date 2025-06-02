from fastapi import APIRouter, HTTPException, Depends
from ..models import MCPMessage, MCPResponse
from ..handlers.search import search_activities
from ..handlers.llama import process_with_llama
from typing import Optional

router = APIRouter()

@router.post("/process", response_model=MCPResponse)
async def process_message(message: MCPMessage):
    try:
        # Process message with Llama
        llama_response = await process_with_llama(message.content)
        
        # Search for relevant activities
        search_results = await search_activities(message.content)
        
        return MCPResponse(
            message_id=message.message_id,
            response=llama_response,
            status="success",
            activities=search_results,
            metadata={
                "source": "activity-agent",
                "processed_with": "llama3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 