from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .handlers.mcp_handler import router as mcp_router
from .utils.config import load_config

app = FastAPI(
    title="Activity Agent",
    description="MCP-compatible activity planning service",
    version="1.0.0"
)

# Load configuration
config = load_config()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mcp_router, prefix="/api/v1", tags=["mcp"])

@app.get("/")
async def root():
    return {"status": "healthy", "service": "activity-agent"} 