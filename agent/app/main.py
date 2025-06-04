# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .summarizer import router as summarizer_router
from .integrations.slack_test import router as slack_test_router
from .integrations.llama_test import router as llama_test_router
from .integrations.questions import router as questions_router
from .integrations.slack_events import router as slack_events_router

app = FastAPI(
    title="WhatsBot",
    description="A Slack bot that can answer questions and summarize text.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include summarizer routes
app.include_router(
    summarizer_router,
    prefix="/api/v1",
    tags=["summarization"]
)

# Include question answering routes
app.include_router(
    questions_router,
    prefix="/api/v1/questions",
    tags=["questions"]
)

# Include Slack events routes
app.include_router(
    slack_events_router,
    prefix="/api/v1",
    tags=["slack"]
)

# Include Slack test routes
app.include_router(
    slack_test_router,
    prefix="/api/v1/integrations",
    tags=["integrations"]
)

# Include Llama test routes
app.include_router(
    llama_test_router,
    prefix="/api/v1/integrations",
    tags=["integrations"]
)

@app.get("/", tags=["health"])
async def root():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "whatsbot",
        "version": "1.0.0"
    }
