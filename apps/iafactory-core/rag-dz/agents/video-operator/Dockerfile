# IA Factory Video Operator
# Agent de Montage Vidéo Automatisé avec IA

FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create directories
RUN mkdir -p /opt/iafactory-rag-dz/uploads/video-operator \
    && mkdir -p /opt/iafactory-rag-dz/outputs/video-operator

# Expose API port
EXPOSE 8080

# Run API server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
