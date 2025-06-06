#!/bin/bash
set -e

echo "Setting OLLAMA_HOST to 0.0.0.0"
export OLLAMA_HOST=0.0.0.0

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "Pulling Llama model..."
ollama pull llama3

echo "Starting Ollama server..."
ollama serve