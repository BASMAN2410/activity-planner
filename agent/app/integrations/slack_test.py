"""
Test endpoints for Slack integration.
"""
from fastapi import APIRouter, HTTPException
from .slack import slack_client

router = APIRouter()

@router.post("/test-slack")
async def test_slack_integration():
    """
    Test the Slack integration by sending a test message.
    """
    try:
        response = await slack_client.post_message(
            channel="all-whatsbot",
            text="🎉 Test message from WhatsBot! If you see this, the Slack integration is working."
        )
        return {
            "status": "success",
            "message": "Test message sent to Slack",
            "slack_response": response
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message to Slack: {str(e)}"
        ) 