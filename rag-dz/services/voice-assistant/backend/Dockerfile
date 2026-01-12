FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV GROQ_API_KEY=""
ENV STT_PROVIDER="groq"
ENV TTS_PROVIDER="edge"
ENV RAG_DZ_URL="http://iaf-rag-prod:3000"
ENV LEGAL_API_URL="http://iaf-legal-assistant-prod:8197"
ENV FISCAL_API_URL="http://iaf-fiscal-assistant-prod:8199"

EXPOSE 8201

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8201"]
