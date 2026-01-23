# Recruteur DZ Agent - Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir streamlit

# Copy agent code
COPY . .

# Copy core module
COPY ../core /app/core

# Expose Streamlit port
EXPOSE 8502

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8502/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "recruteur_ui.py", "--server.port=8502", "--server.address=0.0.0.0", "--server.headless=true"]
