FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Environment variables
ENV PYTHONPATH=/app
ENV USE_SUPABASE=true
ENV SUPABASE_URL=""
ENV SUPABASE_SERVICE_KEY=""
ENV META_URL=http://nexus-meta:8100

EXPOSE 8051

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8051/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8051"]
