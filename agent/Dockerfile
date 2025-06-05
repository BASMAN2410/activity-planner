# Use Python base image
FROM python:3.9-slim

# Install system tools and dependencies
RUN apt-get update && apt-get install -y \
    git \
    net-tools \
    iputils-ping \
    htop \
    vim \
    wget \
    netcat \
    lsof \
    procps \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy startup script
COPY scripts/app-start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["/app/start.sh"] 