from fastapi import APIRouter, HTTPException
from app.models import SummarizationRequest, SummarizationResponse, ErrorResponse
from app.llama import llama
from app.integrations.slack import slack_client
import re
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def count_words(text: str) -> int:
    return len(re.findall(r'\w+', text))

def format_summary(text: str, format_type: str) -> str:
    if format_type == "bullets":
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return "\n".join(f"• {sentence.strip()}" for sentence in sentences if sentence.strip())
    return text

@router.post(
    "/summarize",
    response_model=SummarizationResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    tags=["summarization"]
)
async def summarize_text(request: SummarizationRequest) -> SummarizationResponse:
    """
    Summarize the provided text using the Llama model, then post to Slack.
    """
    try:
        original_length = count_words(request.text)
        if original_length == 0:
            raise HTTPException(status_code=400, detail={"error": "Input text is empty"})

        summary = await llama.summarize(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )

        formatted_summary = format_summary(summary, request.format)
        summary_length = count_words(formatted_summary)

        compression_ratio = round(summary_length / original_length, 2) if original_length else 0

        # 🎯 Post to Slack
        slack_channel = "all-whatsbot"  # Or get from config/env or request!
        await slack_client.post_summary(
            channel=slack_channel,
            original_text=request.text,
            summary=formatted_summary
        )

        return SummarizationResponse(
            summary=formatted_summary,
            original_length=original_length,
            summary_length=summary_length,
            metadata={
                "format": request.format,
                "compression_ratio": compression_ratio
            }
        )

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Summarization failed", "details": str(e)}
        )
