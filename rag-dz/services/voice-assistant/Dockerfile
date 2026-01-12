# DZ-VoiceAssistant API
# Assistant vocal pour iaFactory Algeria - FR + Darija

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .

# Environment variables (overridden at runtime)
ENV GROQ_API_KEY=""
ENV STT_PROVIDER="groq"
ENV TTS_PROVIDER="edge"
ENV RAG_DZ_URL="http://iaf-rag-prod:3000"
ENV LEGAL_API_URL="http://iaf-legal-assistant-prod:8197"
ENV FISCAL_API_URL="http://iaf-fiscal-assistant-prod:8199"

EXPOSE 8201

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8201"]
