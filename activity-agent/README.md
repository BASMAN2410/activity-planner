# Activity Agent

A FastAPI-based service that integrates with MCP (Mission Control Protocol) to handle activity planning requests.

## Features

- FastAPI REST API endpoints for MCP integration
- Llama3 (Ollama) integration for natural language processing
- Search API integration
- Configurable environment variables
- Docker support

## Setup

1. Clone the repository
2. Create a `.env` file with required environment variables
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the service:
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker

Build the container:
```bash
docker build -t activity-agent .
```

Run the container:
```bash
docker run -p 8000:8000 activity-agent
```

## Environment Variables

Create a `.env` file with the following variables:
- `SEARCH_API_KEY`: Your Search API key
- `OLLAMA_API_URL`: URL for Llama3 Ollama instance
- `MCP_API_KEY`: Your MCP API key

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 