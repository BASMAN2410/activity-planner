"""
Slack integration for the summarization service.
"""

import os
import logging
from typing import Dict, Any, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # or DEBUG for local testing

class SlackClient:
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_TOKEN")
        self.base_url = "https://slack.com/api"
        if not self.token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required")

    async def post_message(
        self, channel: str, text: str, thread_ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post a message to a Slack channel.

        :param channel: Slack channel ID or name (e.g., #general or C12345678)
        :param text: Message text
        :param thread_ts: Optional thread timestamp to post as a reply
        :return: Slack API JSON response
        """
        payload = {
            "channel": channel,
            "text": text,
            "unfurl_links": False
        }
        if thread_ts:
            payload["thread_ts"] = thread_ts

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat.postMessage",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("ok"):
                logger.error(f"Slack API error: {data.get('error')}")
                raise Exception(f"Slack API error: {data.get('error')}")

            logger.info(f"Message posted to Slack channel: {channel}")
            return data

    async def post_summary(
        self, channel: str, original_text: str, summary: str, thread_ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post a summary message to a Slack channel with additional stats.

        :param channel: Slack channel ID
        :param original_text: Original text to be summarized
        :param summary: Summarized text
        :param thread_ts: Optional thread timestamp for threading
        :return: Slack API JSON response
        """
        message = (
            f"*Original Text Length:* {len(original_text.split())} words\n"
            f"*Summary Length:* {len(summary.split())} words\n\n"
            f"*Summary:*\n{summary}"
        )
        return await self.post_message(channel, message, thread_ts)

# Global instance for convenient use in other modules
slack_client = SlackClient()
