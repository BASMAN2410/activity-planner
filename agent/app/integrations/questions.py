"""
Question answering integration using Llama.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from ..llama import llama
from ..models import QuestionResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ask", response_model=QuestionResponse)
async def handle_ask(request: Request):
    data = await request.json()
    if "challenge" in data:
        # Slack URL verification
        return JSONResponse(content={"challenge": data["challenge"]})

    # Normal question processing
    try:
        question = data.get("question")
        context = data.get("context")
        format_ = data.get("format", "detailed")

        if not question:
            raise HTTPException(status_code=400, detail="Missing 'question' in request.")

        # Build prompt
        if context:
            prompt = (
                f"Given this context: {context}\n\n"
                f"Please answer this question: {question}\n\n"
                f"If the context doesn't contain enough information, use your knowledge to provide a complete answer."
            )
        else:
            prompt = (
                f"Please answer this question: {question}\n\n"
                f"Provide a {'detailed' if format_ == 'detailed' else 'concise'} answer."
            )

        # Get response from Llama
        response = await llama.generate(prompt=prompt)

        return {
            "status": "success",
            "answer": response,
            "metadata": {
                "format": format_,
                "context_provided": context is not None
            }
        }
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 