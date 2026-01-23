FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir streamlit
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "teaching_assistant_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
