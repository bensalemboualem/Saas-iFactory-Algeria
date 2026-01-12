FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    httpx \
    pydantic \
    pyyaml

# Copy application
COPY backend/ /app/

# Expose port
EXPOSE 8199

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8199"]
