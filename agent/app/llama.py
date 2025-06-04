# app/llama.py

import httpx
import os
import time
import asyncio
from typing import Optional, Dict, Any
import logging
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for maximum verbosity
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class LlamaAPI:
    def __init__(self):
        # URL of the Llama API server
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        # Default model to use
        self.model = os.getenv("OLLAMA_MODEL", "llama3")
        # Number of retries
        self.max_retries = 3
        # Default parameters for generation
        self.default_params = {
            "num_ctx": 512,  # Reduced context window
            "num_predict": 256,  # Limit response length
            "temperature": 0.7,  # Slightly reduced creativity for faster responses
            "top_k": 40,  # Limit token sampling
            "top_p": 0.9,  # Nucleus sampling
            "repeat_penalty": 1.1  # Prevent repetition
        }
        
        logger.info(f"Initializing LlamaAPI with URL: {self.api_url} and model: {self.model}")

    async def _make_request(self, endpoint: str, payload: Dict[str, Any], method: str = "POST") -> Dict[str, Any]:
        """
        Make a request to the Llama API with retries.
        """
        last_error = None
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    if method == "POST":
                        response = await client.post(
                            f"{self.api_url}/{endpoint}",
                            json=payload,
                            timeout=30.0
                        )
                    else:
                        response = await client.get(
                            f"{self.api_url}/{endpoint}",
                            timeout=30.0
                        )
                    
                    response.raise_for_status()
                    return response.json()
            except Exception as e:
                last_error = e
                logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
                continue
        
        raise Exception(f"All requests failed after {self.max_retries} attempts. Last error: {str(last_error)}")

    async def generate(self, prompt: str, **kwargs: Dict[str, Any]) -> str:
        """
        Generate text using the Llama model.
        """
        logger.debug(f"Generating response for prompt: {prompt[:100]}...")
        
        try:
            # Check if the model is available
            models = await self._make_request("api/tags", {}, method="GET")
            available_models = [m.get("name") for m in models.get("models", [])]
            logger.info(f"Available models: {available_models}")
            
            if f"{self.model}:latest" not in available_models:
                raise Exception(f"Model {self.model} not found. Available models: {available_models}")

            # Prepare the request with optimized parameters
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                **self.default_params,  # Add default optimization parameters
                **kwargs  # Allow overriding defaults
            }
            logger.debug(f"Sending request with payload: {json.dumps(payload)[:200]}...")

            # Make the request
            response_data = await self._make_request("api/generate", payload)
            
            if not response_data.get("response"):
                raise Exception(f"No response in output: {response_data}")
            
            logger.info("Successfully generated response")
            return response_data["response"]
            
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")

    async def summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Summarize the given text in a concise manner.
        """
        prompt = (
            "You are a summarization expert. Create clear and concise summaries "
            "that capture the main points while being easy to understand.\n\n"
            f"Please summarize the following text in {min_length}-{max_length} words:\n\n"
            f"{text}\n\n"
            "Summary:"
        )
        
        # Add parameters to optimize for summarization
        params = self.default_params.copy()
        params.update({
            "num_predict": max(100, max_length * 8),  # Adjust based on desired length
            "temperature": 0.5  # More focused for summarization
        })
        
        return await self.generate(prompt, **params)

    async def answer_question(
        self,
        question: str,
        context: Optional[str] = None,
        format: str = "detailed"
    ) -> str:
        """
        Answer a question using the Llama model.

        Args:
            question: The question to answer
            context: Optional context to help answer the question
            format: Response format ('detailed' or 'concise')
        """
        # Add a system prompt to encourage concise responses
        system_prompt = (
            "You are a helpful AI assistant. Provide clear, accurate, and concise answers. "
            "Focus on the most important information and avoid unnecessary details."
        )
        
        if context:
            prompt = (
                f"{system_prompt}\n\n"
                f"Context: {context}\n\n"
                f"Question: {question}\n\n"
                f"Please provide a {'detailed' if format == 'detailed' else 'brief'} answer "
                f"focusing on the most relevant information."
            )
        else:
            prompt = (
                f"{system_prompt}\n\n"
                f"Question: {question}\n\n"
                f"Please provide a {'detailed' if format == 'detailed' else 'brief'} answer "
                f"focusing on the most relevant information."
            )

        # Add parameters to optimize for shorter responses
        params = self.default_params.copy()
        if format == "concise":
            params.update({
                "num_predict": 128,  # Even shorter responses for concise format
                "temperature": 0.5  # More focused responses
            })

        return await self.generate(prompt, **params)

# Create a global instance
llama = LlamaAPI()
