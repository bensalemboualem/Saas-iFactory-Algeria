# Dzir IA Video v2.1 - Quick Deploy (5 minutes)

## 🚀 Fastest Path to Production

### 1. Get Free API Key (2 min)

Visit: https://dashscope.console.aliyun.com/

1. Create free account (email only, no credit card)
2. Go to API Keys section
3. Create new API key
4. Copy the key (starts with `sk-`)

### 2. Configure on VPS (1 min)

```bash
ssh root@46.224.3.125

cd /opt/rag-dz/apps/dzirvideo

# Create .env file
cat > .env << 'EOF'
# Alibaba Cloud (100 free videos/day)
ALIBABA_DASHSCOPE_API_KEY=sk-PASTE-YOUR-KEY-HERE

# YouTube (use existing credentials)
YOUTUBE_CLIENT_ID=existing-value-from-env
YOUTUBE_CLIENT_SECRET=existing-value
YOUTUBE_REFRESH_TOKEN=existing-value

# Free mode
FREE_ONLY_MODE=true
DEFAULT_GENERATOR=wan_2_1
MAX_BUDGET_PER_VIDEO=0.0
API_PORT=8200
LOG_LEVEL=INFO
EOF

# Copy YouTube credentials from existing .env if available
grep "YOUTUBE_" /opt/rag-dz/.env >> .env 2>/dev/null || true
```

### 3. Deploy (2 min)

```bash
# Build and start
docker compose build && docker compose up -d

# Wait 30 seconds for startup
sleep 30

# Verify
curl http://localhost:8200/health
```

Expected output:
```json
{
  "status": "healthy",
  "generators_loaded": 40,
  "default_generator": "wan_2_1"
}
```

### 4. Test Generation (optional)

```bash
# Generate a test video (30-60 seconds)
curl -X POST http://localhost:8200/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over the Sahara desert in Algeria",
    "duration_seconds": 5,
    "category": "text-to-video"
  }'

# Response includes task_id, poll for status
curl http://localhost:8200/api/v1/status/TASK_ID
```

## ✅ Done!

Your Dzir IA Video platform is now live at:
- **API**: https://iafactory.pro/dzirvideo/
- **Docs**: https://iafactory.pro/dzirvideo/docs
- **Frontend**: https://iafactory.pro/dzirvideo/ultimate.html

## 🎯 What You Get (100% Free)

With just the Alibaba API key:

1. **WAN 2.1** (Text-to-Video)
   - 100 videos per day
   - 1080p resolution
   - Quality: 85/100

2. **Qwen 2.1** (Script Optimizer)
   - Unlimited script improvements
   - Multi-language support

3. **Qwen-VL** (Text-to-Image)
   - 100 images per day
   - For thumbnails/frames

**Total Cost**: $0.00/month

## 📊 Upgrade Options (Optional)

Add more free generators:

```bash
# Replicate (pay-as-you-go, $0.002/sec)
REPLICATE_API_TOKEN=r8_xxx

# Kling AI (66 free credits/day ≈ 10 videos)
KLING_AI_API_KEY=xxx

# DIGEN Sora (unlimited free)
# No API key needed, works out of the box
```

## 🐛 Troubleshooting

**Container won't start?**
```bash
docker compose logs dzirvideo
```

**Health check fails?**
```bash
# Check API key format (must start with sk-)
grep ALIBABA .env

# Rebuild without cache
docker compose build --no-cache
docker compose up -d
```

**Out of quota?**
```bash
# Check daily usage
curl https://dashscope.console.aliyun.com/api/usage

# Switch to DIGEN Sora (unlimited free)
curl -X POST http://localhost:8200/api/v1/generate \
  -d '{"prompt": "...", "generator_name": "digen_sora"}'
```

---

**Total Time**: 5 minutes
**Total Cost**: $0
**Videos/Day**: 100+ (free tier)
