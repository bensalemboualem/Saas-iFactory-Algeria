import os
import replicate
from dotenv import load_dotenv

load_dotenv("/opt/iafactory-rag-dz/agents/video-operator/.env")

def create_video(prompt: str) -> str:
    """Create video and return prediction ID"""
    token = os.getenv("REPLICATE_API_TOKEN")
    client = replicate.Client(api_token=token)
    prediction = client.predictions.create(
        model="minimax/video-01",
        input={"prompt": prompt, "prompt_optimizer": True}
    )
    return prediction.id

def get_status(pred_id: str) -> dict:
    """Get prediction status"""
    token = os.getenv("REPLICATE_API_TOKEN")
    client = replicate.Client(api_token=token)
    p = client.predictions.get(pred_id)
    return {
        "status": p.status,
        "output": p.output,
        "error": p.error
    }
