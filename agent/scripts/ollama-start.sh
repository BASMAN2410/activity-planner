#!/bin/bash

# Print banner
echo "Starting WhatsBot Ollama Service"
echo "=============================="

# Start Ollama in the background
echo "Starting Ollama server..."
ollama serve &

# Wait for Ollama to start
echo "Waiting for Ollama to initialize..."
sleep 5

# Pull the required model
echo "Pulling Llama model..."
ollama pull llama3

# Print system information
echo -e "\nSystem Information:"
echo "=================="
echo -e "\nNetwork Interfaces:"
ip addr show

echo -e "\nListening Ports:"
netstat -tulpn

echo -e "\nGPU Information:"
nvidia-smi

echo -e "\nOllama Service Status:"
if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama is running"
    echo "✅ Listening on port 11434"
else
    echo "❌ Ollama failed to start"
    exit 1
fi

echo -e "\nStartup complete! Monitoring logs..."
# Keep container running and show Ollama logs
tail -f /dev/null 