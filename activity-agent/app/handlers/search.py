import httpx
from typing import List, Dict, Any
from ..utils.config import get_settings

async def search_activities(query: str) -> List[Dict[str, Any]]:
    """
    Search for activities using the search API.
    """
    settings = get_settings()
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.search.service/v1/search",
                params={
                    "q": query,
                    "type": "activity"
                },
                headers={
                    "Authorization": f"Bearer {settings.search_api_key}"
                }
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except httpx.HTTPError as e:
            # Log the error and return empty results
            print(f"Search API error: {str(e)}")
            return [] 