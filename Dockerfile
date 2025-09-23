FROM python:3.9-slim

# Force rebuild - cache bust
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variables
ENV ENVIRONMENT=production

# Start command - use Railway's PORT environment variable with debug logging
CMD ["sh", "-c", "echo 'Starting app on port $PORT' && uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080} --log-level debug"]
