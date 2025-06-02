import httpx
from ..utils.config import get_settings

async def process_with_llama(content: str) -> str:
    """
    Process the input content with Llama3 using Ollama.
    """
    settings = get_settings()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ollama_api_url}/api/generate",
                json={
                    "model": "llama3",
                    "prompt": content,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except httpx.HTTPError as e:
            print(f"Llama API error: {str(e)}")
            return "Error processing with language model" 