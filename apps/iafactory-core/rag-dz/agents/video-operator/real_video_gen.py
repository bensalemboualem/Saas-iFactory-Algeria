import os
import replicate
import httpx
from dotenv import load_dotenv

load_dotenv()

REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")

async def generate_real_video(prompt: str, duration: int = 5) -> dict:
    """Generate real video using Replicate Minimax model"""
    
    if not REPLICATE_TOKEN:
        return {"error": "REPLICATE_API_TOKEN not configured"}
    
    try:
        # Use minimax video-01 model
        client = replicate.Client(api_token=REPLICATE_TOKEN)
        
        # Create prediction
        prediction = client.predictions.create(
            model="minimax/video-01",
            input={
                "prompt": prompt,
                "prompt_optimizer": True
            }
        )
        
        return {
            "prediction_id": prediction.id,
            "status": prediction.status,
            "model": "minimax/video-01"
        }
        
    except Exception as e:
        return {"error": str(e)}

async def check_prediction_status(prediction_id: str) -> dict:
    """Check status of a Replicate prediction"""
    
    if not REPLICATE_TOKEN:
        return {"error": "REPLICATE_API_TOKEN not configured"}
    
    try:
        client = replicate.Client(api_token=REPLICATE_TOKEN)
        prediction = client.predictions.get(prediction_id)
        
        result = {
            "id": prediction.id,
            "status": prediction.status,
            "created_at": str(prediction.created_at),
        }
        
        if prediction.status == "succeeded":
            result["video_url"] = prediction.output
            
        if prediction.status == "failed":
            result["error"] = prediction.error
            
        return result
        
    except Exception as e:
        return {"error": str(e)}

# Test
if __name__ == "__main__":
    import asyncio
    result = asyncio.run(generate_real_video("A beautiful sunset over the ocean"))
    print(result)
ENDSCRIPT
