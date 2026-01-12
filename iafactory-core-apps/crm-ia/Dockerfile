FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create upload directory
RUN mkdir -p /app/uploads

# Copy application
COPY crm_api.py .

# Environment
ENV UPLOAD_DIR=/app/uploads

# Expose port
EXPOSE 8212

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8212/health', timeout=5)" || exit 1

# Run application
CMD ["uvicorn", "crm_api:app", "--host", "0.0.0.0", "--port", "8212"]
