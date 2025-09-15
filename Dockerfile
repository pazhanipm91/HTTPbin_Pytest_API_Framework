# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test framework code
COPY . .

# Default command (can be overridden by docker-compose)
CMD ["pytest", "-v", "--alluredir=/reports"]
