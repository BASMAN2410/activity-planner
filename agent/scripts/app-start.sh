#!/bin/bash

# Print banner
echo "Starting WhatsBot Application"
echo "==========================="

# Print system information
echo -e "\nSystem Information:"
echo "=================="
echo -e "\nNetwork Interfaces:"
ip addr show

echo -e "\nListening Ports:"
netstat -tulpn

# Check Ollama connectivity
echo -e "\nChecking Ollama connectivity:"
for i in {1..5}; do
    if nc -z 3vsrtr8cbw2o8t-11434.proxy.runpod.net 443; then
        echo "✅ Successfully connected to Ollama service"
        break
    fi
    if [ $i -eq 5 ]; then
        echo "❌ Failed to connect to Ollama service after 5 attempts"
        echo "Please check if the Ollama service is running and network configuration is correct"
        exit 1
    fi
    echo "Attempt $i: Waiting for Ollama service to become available..."
    sleep 5
done

# Test Ollama API
echo -e "\nTesting Ollama API:"
curl -s "https://3vsrtr8cbw2o8t-11434.proxy.runpod.net/api/tags" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Ollama API is responding"
else
    echo "❌ Ollama API is not responding"
    echo "Please check if the Ollama service is running correctly"
    exit 1
fi

echo -e "\nStarting FastAPI application..."
# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 