# Use an official Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && rm -rf /var/lib/apt/lists/*

# Install UV (Python package manager)
RUN pip install uv

# Copy pyproject.toml (if you have one)  # Execute again only if some requirements changes
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application files  # Execute again if application files change
COPY . .

# Set environment variables (optional defaults)
ENV PYTHONUNBUFFERED=1
ENV TELEGRAM_BOT_TOKEN=""
ENV NOTION_TOKEN=""
ENV NOTION_DB_ID=""
ENV LLM_PROVIDER=""
ENV GEMINI_API_KEY=""
ENV ANTHROPIC_API_KEY=""
ENV OPENAI_API_KEY=""

# Run the application
CMD ["uv", "run", "python", "think_drop/main.py"]
