# Dzir IA Video v2.1 - Multi-Generator AI Video Platform
# 40+ AI generators (text-to-video, text-to-image, reels, avatars)
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    espeak-ng \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install torch CPU with PINNED versions (avoid installation freeze)
RUN pip install --no-cache-dir --default-timeout=900 \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.1.0+cpu torchaudio==2.1.0+cpu

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=900 -r requirements.txt

# Download TTS model (French)
RUN python -c "from TTS.api import TTS; TTS('tts_models/fr/css10/vits')"

# Copy application code
COPY . .

# Create output directories
RUN mkdir -p output/videos output/audio output/subtitles models

# Expose API port
EXPOSE 8200

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8200/health')"

# Run FastAPI server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8200", "--reload"]
