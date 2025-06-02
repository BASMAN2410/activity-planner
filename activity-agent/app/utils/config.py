from pydantic import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    search_api_key: str
    ollama_api_url: str = "http://localhost:11434"
    mcp_api_key: str
    log_level: str = "INFO"
    port: int = 8000

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

def load_config() -> Settings:
    """
    Load and validate configuration from environment variables.
    """
    settings = get_settings()
    
    # Validate required settings
    if not settings.search_api_key:
        raise ValueError("SEARCH_API_KEY must be set")
    if not settings.mcp_api_key:
        raise ValueError("MCP_API_KEY must be set")
        
    return settings 