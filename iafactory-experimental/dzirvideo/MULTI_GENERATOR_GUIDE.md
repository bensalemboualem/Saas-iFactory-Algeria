# Dzir IA Video v2.1 - Multi-Generator System Guide

## 🎯 Overview

**Dzir IA Video v2.1** is a comprehensive video generation platform integrating **31 AI generators** across **6 categories**, providing automated selection of the optimal generator for any task.

### Key Features

- **31 AI Generators** (13 free, 12 freemium, 6 premium)
- **Smart Router** - Automatic optimal generator selection
- **Cost Tracking** - Budget management and estimation
- **Comparison Mode** - Generate with multiple AIs side-by-side
- **REST API** - Complete FastAPI integration
- **Free Tier Priority** - Alibaba WAN 2.1, Qwen-VL, FLUX.1, DIGEN Sora

---

## 📊 Generator Categories

### 1. Text-to-Video (12 generators)

| Generator | Provider | Quality | Cost/s | Free Tier | Max Duration |
|-----------|----------|---------|--------|-----------|--------------|
| WAN 2.1 | Alibaba Cloud | 85 | $0.00 | ✅ 100/day | 10s |
| Kling AI | Kuaishou | 90 | $0.01 | ✅ 66/day | 120s |
| Pika Labs | Pika | 87 | $0.015 | ✅ 250 credits | 30s |
| Luma Dream | Luma AI | 90 | $0.02 | ✅ 30/month | 5s |
| Hailuo AI | Minimax | 88 | $0.008 | ✅ 50 credits | 6s |
| Runway Gen-4 | Runway ML | 95 | $0.05 | ❌ | 60s |
| Veo 2 | Google DeepMind | 93 | $0.50 | ❌ | 30s |
| Sora | OpenAI | 94 | $0.30 | ❌ | 20s |
| LTX Studio | LTX | 93 | $0.03 | ❌ | 120s |
| CogVideo | Zhipu AI | 78 | FREE | ✅ | 8s |
| Open-Sora | Community | 75 | FREE | ✅ | 16s |
| StarryAI | StarryAI | 86 | $0.02 | ✅ 5/day | 10s |

### 2. Text-to-Image (6 generators)

| Generator | Provider | Quality | Cost/img | Free Tier | Resolution |
|-----------|----------|---------|----------|-----------|------------|
| Qwen-VL | Alibaba Cloud | 80 | $0.00 | ✅ 200/day | 1024x1024 |
| FLUX.1 | Black Forest Labs | 90 | $0.00 | ✅ Unlimited | 1024x1024 |
| DALL-E 3 | OpenAI | 93 | $0.04 | ❌ | 1024x1024 |
| Midjourney | Midjourney | 97 | $0.05 | ❌ | 1024x1024 |
| Ideogram | Ideogram | 89 | $0.025 | ✅ 25/day | 1024x1024 |
| Leonardo AI | Leonardo | 87 | $0.01 | ✅ 150/day | 1024x1024 |

### 3. Image-to-Video (1 generator)

| Generator | Provider | Quality | Cost/s | Free Tier | Max Duration |
|-----------|----------|---------|--------|-----------|--------------|
| Stable Video Diffusion | Stability AI | 85 | FREE | ✅ Unlimited | 3s |

### 4. Avatar Video (5 generators)

| Generator | Provider | Quality | Cost/s | Free Tier | Use Case |
|-----------|----------|---------|--------|-----------|----------|
| Vidnoz | Vidnoz | 85 | $0.01 | ✅ 10/day | Avatars + voice |
| DeepBrain AI | DeepBrain | 95 | $0.02 | ❌ | TV presenters |
| Elai.io | Elai | 88 | $0.015 | ✅ 5/day | Text→video avatars |
| HeyGen | HeyGen | 92 | $0.02 | ✅ 3/day | Enterprise avatars |
| Synthesia | Synthesia | 93 | $0.03 | ❌ | Training/corporate |

### 5. Reels/Short-form (6 generators)

| Generator | Provider | Quality | Cost | Free Tier | Specialty |
|-----------|----------|---------|------|-----------|-----------|
| DIGEN Sora | DIGEN | 78 | FREE | ✅ Unlimited | Shorts/TikTok |
| Pictory | Pictory.ai | 80 | Subscription | ✅ 3 videos | Article→video |
| CapCut | ByteDance | 92 | FREE/Pro | ✅ Unlimited | TikTok/Reels editing |
| Lumen5 | Lumen5 | 82 | FREE | ✅ 5/day | Blog→social media |
| Descript | Descript | 91 | $0.01/s | ✅ 3/day | Editing + overdub |
| InVideo AI | InVideo | 84 | $0.01/s | ✅ 10/day | Marketing videos |

### 6. AI Assistant (1 optimizer)

| Tool | Provider | Function | Cost | Free Tier |
|------|----------|----------|------|-----------|
| Qwen Optimizer | Alibaba Cloud | Script optimization | FREE | ✅ Unlimited |

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
cd d:/IAFactory/rag-dz/apps/dzirvideo
pip install -r requirements.txt
```

### 2. API Keys Setup

Create `.env` file:

```bash
# Alibaba Cloud (Priority - FREE)
ALIBABA_DASHSCOPE_API_KEY=sk-xxxxxx

# Optional generators
KLING_AI_API_KEY=xxxx
PIKA_API_KEY=xxxx
LUMA_API_KEY=xxxx
RUNWAY_API_KEY=xxxx
OPENAI_API_KEY=xxxx
REPLICATE_API_TOKEN=xxxx
TOGETHER_API_KEY=xxxx
```

### 3. Start API Server

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8200 --reload
```

### 4. Test Endpoints

```bash
# List all generators
curl http://localhost:8200/api/v1/generators/list

# Get generator info
curl http://localhost:8200/api/v1/generators/info/wan_2_1

# Get summary
curl http://localhost:8200/api/v1/generators/summary
```

---

## 🎮 Usage Examples

### Example 1: Auto-Route (Smart Selection)

```python
import requests

response = requests.post("http://localhost:8200/api/v1/generators/generate", json={
    "prompt": "A serene sunset over the Algerian Sahara desert",
    "category": "text-to-video",
    # generator_name not specified = auto-route
    "duration_seconds": 10,
    "max_budget_usd": 0,  # Free only
    "quality_priority": True
})

result = response.json()
print(f"Selected generator: {result['generator_name']}")
# Expected: wan_2_1 (best free option)
print(f"Task ID: {result['task_id']}")
```

### Example 2: Specific Generator

```python
response = requests.post("http://localhost:8200/api/v1/generators/generate", json={
    "prompt": "Professional CEO presenting quarterly results",
    "category": "avatar-video",
    "generator_name": "heygen",  # Explicitly use HeyGen
    "duration_seconds": 30
})
```

### Example 3: Comparison Mode

```python
response = requests.post("http://localhost:8200/api/v1/generators/compare", json={
    "prompt": "A futuristic city in Algeria in 2050",
    "category": "text-to-video",
    "generators": ["wan_2_1", "kling_ai", "luma_dream", "runway_gen4"],
    "duration_seconds": 10
})

# Returns task IDs for all 4 generators
results = response.json()
for gen, data in results['generators'].items():
    print(f"{gen}: Task {data['task_id']}")
```

### Example 4: Get Recommendation

```python
response = requests.post("http://localhost:8200/api/v1/generators/recommend", json={
    "category": "text-to-image",
    "budget_level": "free"  # free | budget | premium
})

rec = response.json()
print(f"Primary: {rec['primary_recommendation']['name']}")
print(f"Quality: {rec['primary_recommendation']['quality']}")
print(f"Cost: ${rec['primary_recommendation']['cost_per_image']}")
```

### Example 5: Check Status

```python
response = requests.get(
    f"http://localhost:8200/api/v1/generators/status/wan_2_1/{task_id}"
)

status = response.json()
if status['status'] == 'completed':
    print(f"Video URL: {status['output_url']}")
else:
    print(f"Progress: {status['progress_percentage']}%")
```

---

## 🔧 Python SDK Usage

### Direct Generator Usage

```python
from generators.registry import get_global_registry
from generators.base import GenerationRequest, GeneratorCategory

# Get registry
registry = get_global_registry()

# Get generator
generator = registry.get("wan_2_1", api_key="sk-xxxx")

# Create request
request = GenerationRequest(
    prompt="Beautiful Algerian landscape",
    category=GeneratorCategory.TEXT_TO_VIDEO,
    duration_seconds=10,
    aspect_ratio="9:16"
)

# Generate
result = await generator.generate(request)
print(f"Task ID: {result.task_id}")

# Check status
status = await generator.check_status(result.task_id)
if status.status == GenerationStatus.COMPLETED:
    print(f"Done: {status.output_url}")
```

### Smart Router Usage

```python
from generators.router import SmartRouter, RoutingCriteria
from generators.base import GeneratorCategory, GenerationRequest

router = SmartRouter()

# Route with criteria
criteria = RoutingCriteria(
    category=GeneratorCategory.TEXT_TO_VIDEO,
    max_cost_usd=0.0,  # Free only
    quality_priority=True,
    min_quality_score=80
)

request = GenerationRequest(
    prompt="Algerian street food preparation",
    category=GeneratorCategory.TEXT_TO_VIDEO,
    duration_seconds=15
)

generator_name = router.route(request, criteria)
print(f"Optimal generator: {generator_name}")
```

### Convenience Functions

```python
from generators.router import auto_route
from generators.base import GeneratorCategory

# Simplest usage
generator_name = auto_route(
    prompt="Ancient ruins of Timgad, Algeria",
    category=GeneratorCategory.TEXT_TO_VIDEO,
    budget=0,  # Free only
    duration_seconds=10
)

# Use generator
from generators.registry import get_global_registry
registry = get_global_registry()
generator = registry.get(generator_name)
result = await generator.generate(...)
```

---

## 📐 Architecture

```
Dzir IA Video v2.1 Architecture
│
├── API Layer (FastAPI)
│   ├── /api/v1/generators/*  ← REST endpoints
│   └── api_generators.py      ← Request/response models
│
├── Routing Layer
│   ├── SmartRouter            ← Auto-selection logic
│   ├── RoutingCriteria        ← Selection parameters
│   └── Scoring Algorithm      ← Quality/cost/speed scoring
│
├── Registry Layer
│   ├── GeneratorRegistry      ← Central generator database
│   ├── get_global_registry()  ← Singleton access
│   └── Metadata Management    ← Provider, tags, enabled status
│
├── Base Layer
│   ├── BaseGenerator          ← Abstract base class
│   ├── GeneratorCapabilities  ← Metadata dataclass
│   ├── GenerationRequest      ← Input model
│   └── GenerationResult       ← Output model
│
└── Generator Implementations (31)
    ├── text_to_video/         ← 12 generators
    ├── text_to_image/         ← 6 generators
    ├── image_to_video/        ← 1 generator
    ├── avatar_video/          ← 5 generators
    └── reels_shortform/       ← 6 generators
```

---

## 🧪 Testing

### Unit Tests (Example)

```python
import pytest
from generators.text_to_video.wan_2_1 import WAN21Generator
from generators.base import GenerationRequest, GeneratorCategory

@pytest.mark.asyncio
async def test_wan_21_generation():
    generator = WAN21Generator(api_key="test-key")

    request = GenerationRequest(
        prompt="Test video",
        category=GeneratorCategory.TEXT_TO_VIDEO,
        duration_seconds=5
    )

    result = await generator.generate(request)
    assert result.task_id is not None
    assert result.status == GenerationStatus.PROCESSING
```

### Integration Tests

```bash
# Test all free generators
pytest tests/integration/test_free_generators.py

# Test smart routing
pytest tests/integration/test_smart_router.py

# Test API endpoints
pytest tests/integration/test_api_endpoints.py
```

---

## 💰 Cost Optimization Strategies

### Strategy 1: Free-Only Mode

```python
# Only use 100% free generators
criteria = RoutingCriteria(
    category=GeneratorCategory.TEXT_TO_VIDEO,
    free_only=True
)
```

**Available free generators:**
- WAN 2.1 (100 videos/day)
- DIGEN Sora (unlimited)
- CogVideo (self-hosted)
- Open-Sora (self-hosted)
- Qwen-VL images (200/day)
- FLUX.1 images (unlimited)

### Strategy 2: Budget Cap

```python
# Cap spending at $0.10 per generation
criteria = RoutingCriteria(
    category=GeneratorCategory.TEXT_TO_VIDEO,
    max_cost_usd=0.10
)
```

### Strategy 3: Cascade Fallback

```python
# Try free, then cheap, then premium
fallback_order = [
    "wan_2_1",        # Free
    "hailuo_ai",      # $0.008/s (cheapest paid)
    "kling_ai",       # $0.01/s
    "runway_gen4"     # $0.05/s (best quality)
]

generator_name = router.route(request, criteria, fallback_order=fallback_order)
```

---

## 🔒 Security & API Key Management

### Best Practices

1. **Never commit `.env` file**
```bash
# Add to .gitignore
.env
.env.local
*.key
```

2. **Use environment variables**
```python
import os
api_key = os.getenv("ALIBABA_DASHSCOPE_API_KEY")
```

3. **Rotate keys regularly**
```bash
# Revoke old key in provider dashboard
# Generate new key
# Update .env
```

4. **Monitor usage**
```python
from generators.registry import get_global_registry
registry = get_global_registry()
summary = registry.get_summary()
print(f"Total generators: {summary['total_generators']}")
```

---

## 📈 Performance Optimization

### Parallel Generation

```python
import asyncio

async def generate_batch(prompts: list):
    tasks = []
    for prompt in prompts:
        generator = registry.get("wan_2_1")
        request = GenerationRequest(prompt=prompt, ...)
        tasks.append(generator.generate(request))

    results = await asyncio.gather(*tasks)
    return results

# Generate 10 videos in parallel
prompts = ["Scene 1", "Scene 2", ...]
results = await generate_batch(prompts)
```

### Caching

```python
# Registry caches generator instances
generator1 = registry.get("wan_2_1")  # Creates instance
generator2 = registry.get("wan_2_1")  # Returns cached instance
assert generator1 is generator2  # True
```

---

## 🐛 Troubleshooting

### Issue 1: "Generator not found"

```python
# Check if generator is registered
from generators.registry import get_global_registry
registry = get_global_registry()
print(registry.list_all())
```

### Issue 2: "API key required"

```python
# Verify environment variable
import os
print(os.getenv("ALIBABA_DASHSCOPE_API_KEY"))

# Provide key explicitly
generator = registry.get("wan_2_1", api_key="sk-xxxx")
```

### Issue 3: "Quota exceeded"

```python
from generators.base import QuotaExceededError

try:
    result = await generator.generate(request)
except QuotaExceededError as e:
    print(f"Quota exceeded: {e}")
    # Switch to different generator
    generator = registry.get("kling_ai")
```

---

## 📚 API Reference

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/generators/list` | List all generators |
| GET | `/api/v1/generators/info/{name}` | Get generator details |
| GET | `/api/v1/generators/summary` | Get statistics |
| POST | `/api/v1/generators/generate` | Generate content |
| GET | `/api/v1/generators/status/{name}/{task_id}` | Check status |
| POST | `/api/v1/generators/cancel/{name}/{task_id}` | Cancel generation |
| POST | `/api/v1/generators/compare` | Multi-generator comparison |
| POST | `/api/v1/generators/recommend` | Get recommendations |
| GET | `/api/v1/generators/estimate-cost/{name}` | Estimate cost |

### Python Classes

| Class | Module | Purpose |
|-------|--------|---------|
| `BaseGenerator` | `generators.base` | Abstract generator interface |
| `GeneratorRegistry` | `generators.registry` | Generator management |
| `SmartRouter` | `generators.router` | Auto-selection logic |
| `GenerationRequest` | `generators.base` | Input model |
| `GenerationResult` | `generators.base` | Output model |
| `RoutingCriteria` | `generators.router` | Selection criteria |

---

## 🎯 Next Steps

1. **Add Remaining Generators** (9 from original plan)
   - HunyuanVideo, Mochi 1, Vidu AI, Pollo AI, Krea Video, Canva AI, Adobe Firefly, Playground v2, Stable Diffusion 3.5

2. **Frontend Integration**
   - Create `public/index-ultimate.html` with generator selector
   - Add comparison mode UI (4 results side-by-side)
   - Display cost estimates in real-time

3. **Pipeline v2**
   - Integrate multi-generators into main YouTube Shorts pipeline
   - Scene-based video generation (split script → generate clips → assemble)
   - Automatic B-roll insertion

4. **Monitoring**
   - Add Prometheus metrics
   - Track generator usage and costs
   - Alert on quota limits

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 👥 Contributors

- IAFactory Team

## 🔗 Links

- **Documentation**: [GENERATORS_IMPLEMENTED.md](GENERATORS_IMPLEMENTED.md)
- **API Docs**: http://localhost:8200/docs (when server running)
- **GitHub**: https://github.com/iafactory/rag-dz

---

**Version**: v2.1.0
**Last Updated**: 2025-12-13
**Total Generators**: 31
**Total Code**: ~8,000+ lines
