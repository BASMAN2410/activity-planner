# WhatsBot

A Slack bot that can answer questions and summarize text using Llama model.

## Features
- Responds to @whatsbot mentions in Slack
- Provides concise answers using Llama model
- Supports threaded conversations
- Optimized for performance with configurable parameters

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
SLACK_BOT_TOKEN=your-slack-bot-token
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Deploying to Runpod.io

1. Build the Docker image:
```bash
docker build -t whatsbot:latest .
```

2. Push to your container registry:
```bash
docker tag whatsbot:latest your-registry/whatsbot:latest
docker push your-registry/whatsbot:latest
```

3. Deploy on Runpod.io:
- Go to runpod.io and create a new pod
- Use the provided `runpod-template.json` configuration
- Update the environment variables with your Slack bot token
- Select appropriate GPU template (recommended: RTX 4000 or better)
- Deploy the pod

4. Configure Slack:
- Go to your Slack App settings
- Under "Event Subscriptions", enable events
- Add your pod's URL: `https://your-pod-url/api/v1/slack/events`
- Subscribe to the `app_mention` event
- Reinstall your app if prompted

## Environment Variables

- `SLACK_BOT_TOKEN`: Your Slack bot's OAuth token
- `OLLAMA_API_URL`: URL of the Ollama API (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: llama3)

## API Endpoints

- `POST /api/v1/slack/events`: Handles Slack events
- `POST /api/v1/questions/ask`: Question answering endpoint
- `POST /api/v1/summarize`: Text summarization endpoint
- `GET /`: Health check endpoint 