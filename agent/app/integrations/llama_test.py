"""
Test endpoints for Llama integration.
"""
from fastapi import APIRouter, HTTPException
from ..llama import llama

router = APIRouter()

@router.post("/test-llama")
async def test_llama_connection():
    """
    Test the Llama integration by generating a simple response.
    """
    try:
        response = await llama.generate(
            prompt="Say 'Hello! I am working!' if you can read this message."
        )
        return {
            "status": "success",
            "message": "Llama connection test successful",
            "llama_response": response
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Llama: {str(e)}"
        ) 