FROM python:3.12-slim

# Prevent Python from writing .pyc files and make logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first for better Docker cache.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only the files needed by the agent.
COPY src/ ./src/
COPY config/ ./config/
COPY README.md .
COPY .env.example .

# Create logs directory inside the container.
RUN mkdir -p logs

# Run as a non-root user for safer execution.
RUN useradd --create-home --shell /bin/bash agentuser
RUN chown -R agentuser:agentuser /app

USER agentuser

CMD ["python", "src/main.py"]