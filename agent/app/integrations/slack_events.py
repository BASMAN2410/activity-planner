"""
Slack Events API handler for WhatsBot.
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from ..llama import llama
from ..integrations.slack import slack_client
import logging
from typing import Dict, Any

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/slack/events")
async def handle_slack_events(request: Request):
    """
    Handle incoming Slack events, particularly app_mention events.
    """
    try:
        body = await request.json()
        
        # Handle Slack URL verification
        if body.get("type") == "url_verification":
            return {"challenge": body["challenge"]}
            
        # Process events
        event = body.get("event", {})
        event_type = event.get("type")
        
        if event_type == "app_mention":
            return await handle_app_mention(event)
            
        return {"status": "ignored", "event_type": event_type}
        
    except Exception as e:
        logger.error(f"Error processing Slack event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_app_mention(event: Dict[str, Any]):
    """
    Handle when @whatsbot is mentioned in a channel.
    """
    try:
        # Extract the message text, removing the bot mention
        text = event["text"]
        # Remove <@BOTID> from the text
        question = text.split(">", 1)[1].strip() if ">" in text else text.strip()
        
        if not question:
            response_text = "Hello! How can I help you today?"
        else:
            # Generate response using Llama
            try:
                response = await llama.answer_question(
                    question=question,
                    format="concise"  # Use concise format for Slack
                )
                response_text = response
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                response_text = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."

        # Post response back to Slack
        await slack_client.post_message(
            channel=event["channel"],
            text=response_text,
            thread_ts=event.get("thread_ts") or event.get("ts")  # Reply in thread if available
        )
        
        return {"status": "success", "message": "Response sent to Slack"}
        
    except Exception as e:
        logger.error(f"Error handling app mention: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 