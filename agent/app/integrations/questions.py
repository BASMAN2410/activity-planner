"""
Question answering integration using Llama.
"""
from fastapi import APIRouter, HTTPException
from ..llama import llama
from ..models import QuestionRequest, QuestionResponse
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/ask", response_model=QuestionResponse)
async def answer_question(request: QuestionRequest):
    """
    Answer a user's question using the Llama model.
    """
    try:
        logger.info(f"Received question request: {request.question[:100]}...")
        
        # Construct the prompt based on whether context is provided
        if request.context:
            prompt = (
                f"Given this context: {request.context}\n\n"
                f"Please answer this question: {request.question}\n\n"
                f"If the context doesn't contain enough information, use your knowledge to provide a complete answer."
            )
        else:
            prompt = (
                f"Please answer this question: {request.question}\n\n"
                f"Provide a {'detailed' if request.format == 'detailed' else 'concise'} answer."
            )

        logger.debug(f"Generated prompt: {prompt[:100]}...")

        # Get response from Llama
        try:
            response = await llama.generate(prompt=prompt)
            logger.info("Successfully generated response from Llama")
        except Exception as e:
            logger.error(f"Error generating response from Llama: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate response: {str(e)}"
            )

        return {
            "status": "success",
            "answer": response,
            "metadata": {
                "format": request.format,
                "context_provided": request.context is not None
            }
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error in answer_question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        ) 