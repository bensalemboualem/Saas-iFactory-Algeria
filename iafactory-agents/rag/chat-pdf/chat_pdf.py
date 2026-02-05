import os
import tempfile
import streamlit as st
from embedchain import App

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:3001")

def embedchain_bot(db_path):
    """Configure Embedchain to route LLM calls through the gateway.
    Embedchain's OpenAI provider supports base_url override."""
    return App.from_config(
        config={
            "llm": {
                "provider": "openai",
                "config": {
                    "api_key": "gateway",
                    "model": "gpt-4o",
                    "api_base": f"{GATEWAY_URL}/v1",
                },
            },
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {
                "provider": "openai",
                "config": {
                    "api_key": os.getenv("OPENAI_API_KEY", "gateway"),
                },
            },
        }
    )

st.title("Chat with PDF")

db_path = tempfile.mkdtemp()
app = embedchain_bot(db_path)

if True:

    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    if pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf_file.getvalue())
            app.add(f.name, data_type="pdf_file")
        os.remove(f.name)
        st.success(f"Added {pdf_file.name} to knowledge base!")

    prompt = st.text_input("Ask a question about the PDF")

    if prompt:
        answer = app.chat(prompt)
        st.write(answer)

        