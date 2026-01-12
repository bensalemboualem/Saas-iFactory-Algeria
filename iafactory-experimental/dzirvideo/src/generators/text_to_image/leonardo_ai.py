"""
Leonardo AI - Creative AI Art Generation
High-quality AI art with fine-tuned models
Official: https://leonardo.ai/
"""

import os, logging
from typing import Optional
import requests
from ..base import *

logger = logging.getLogger(__name__)


class LeonardoAIGenerator(BaseGenerator):
    """Leonardo AI - Art IA créatif avec modèles fine-tunés"""

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv("LEONARDO_API_KEY")
        if not self.api_key:
            raise ValueError("Leonardo AI API key required")
        self.api_base = "https://cloud.leonardo.ai/api/rest/v1"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _define_capabilities(self) -> GeneratorCapabilities:
        return GeneratorCapabilities(
            supports_text_to_image=True, max_resolution="1024x1024",
            api_cost_per_image=0.01, free_tier=True, free_credits_per_day=150,
            quality_score=87, avg_generation_time_seconds=20.0
        )

    async def generate(self, request: GenerationRequest) -> GenerationResult:
        self.validate_request(request)
        resp = self.session.post(
            f"{self.api_base}/generations",
            json={"prompt": request.prompt, "num_images": 1, "width": 1024, "height": 1024},
            timeout=30
        )
        if resp.status_code != 200:
            raise APIError(f"Leonardo error: {resp.text}")
        task_id = resp.json().get("sdGenerationJob", {}).get("generationId")
        return GenerationResult(status=GenerationStatus.PROCESSING, task_id=task_id, estimated_completion_time=20.0)

    async def check_status(self, task_id: str) -> GenerationResult:
        resp = self.session.get(f"{self.api_base}/generations/{task_id}", timeout=10)
        data = resp.json().get("generations_by_pk", {})
        status = GenerationStatus.COMPLETED if data.get("status") == "COMPLETE" else GenerationStatus.PROCESSING
        result = GenerationResult(status=status, task_id=task_id)
        if status == GenerationStatus.COMPLETED:
            images = data.get("generated_images", [])
            if images:
                result.output_url = images[0].get("url")
        return result

    async def cancel(self, task_id: str) -> bool:
        return False

    def __str__(self) -> str:
        return "LeonardoAIGenerator(Freemium, Quality=87)"
