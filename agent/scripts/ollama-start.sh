#!/bin/bash
set -e

echo "Setting OLLAMA_HOST to 0.0.0.0"
export OLLAMA_HOST=0.0.0.0

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "Updating PATH to include /usr/local/bin"
export PATH=$PATH:/usr/local/bin

echo "Starting Ollama server in background..."
ollama serve &

# Wait for server to come up
echo "Waiting for Ollama server to be ready..."
sleep 20

echo "Pulling Llama model..."
ollama pull llama3

echo "Ollama server and Llama model are ready."
# Keep the server running in the foreground
wait