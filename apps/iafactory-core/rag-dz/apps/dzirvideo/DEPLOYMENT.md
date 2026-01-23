# Dzir IA Video v2.1 - Deployment Guide

## 🚀 Quick Deploy to VPS

### Prerequisites

1. **VPS Access**: SSH access to `root@46.224.3.125`
2. **API Keys**: At minimum, get Alibaba Cloud API key (free tier)
3. **YouTube OAuth**: Configured refresh token

### One-Command Deploy

```bash
# From local machine (Windows)
cd d:\IAFactory\rag-dz\apps\dzirvideo
bash deploy-to-vps.sh
```

This will:
1. Sync code to VPS via rsync
2. Build Docker image on VPS
3. Start containers
4. Run health checks

## 📋 Manual Deployment Steps

### 1. Local Build (Optional - Test First)

```bash
# Build locally to test
docker compose build

# Test locally
docker compose up -d
curl http://localhost:8200/health

# Should return: {"status": "healthy", "generators_loaded": 40}
```

### 2. Sync to VPS

```bash
# Sync code (excludes output/, models/, cache/)
rsync -avz --progress \
    --exclude 'output/' \
    --exclude 'models/' \
    --exclude '__pycache__/' \
    --exclude '.git/' \
    --exclude '.env' \
    . root@46.224.3.125:/opt/rag-dz/apps/dzirvideo/
```

### 3. Configure Environment on VPS

```bash
# SSH to VPS
ssh root@46.224.3.125

cd /opt/rag-dz/apps/dzirvideo

# Copy .env template
cp .env.example .env

# Edit with your API keys
nano .env
```

**Minimum Required Variables:**
```bash
# Alibaba Cloud (FREE - get from https://dashscope.console.aliyun.com/)
ALIBABA_DASHSCOPE_API_KEY=sk-xxx

# YouTube API (for upload)
YOUTUBE_CLIENT_ID=xxx.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=xxx
YOUTUBE_REFRESH_TOKEN=xxx

# App Config
API_PORT=8200
FREE_ONLY_MODE=true  # Use only free generators
DEFAULT_GENERATOR=wan_2_1  # Alibaba WAN 2.1
```

### 4. Build on VPS

```bash
# Build Docker image (takes ~5-10 minutes)
docker compose build --progress=plain 2>&1 | tee build.log

# Check build succeeded
tail -20 build.log
```

### 5. Start Containers

```bash
# Start in detached mode
docker compose up -d

# Check logs
docker compose logs -f dzirvideo

# Verify health
curl http://localhost:8200/health
```

Expected response:
```json
{
  "status": "healthy",
  "generators_loaded": 40,
  "free_generators": 8,
  "default_generator": "wan_2_1",
  "version": "2.1.0"
}
```

### 6. Configure Nginx Reverse Proxy

Add to `/etc/nginx/sites-available/iafactory.conf`:

```nginx
# Dzir IA Video v2.1
location /dzirvideo/ {
    proxy_pass http://localhost:8200/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;

    # Increased timeouts for video generation (up to 10 minutes)
    proxy_connect_timeout 600;
    proxy_send_timeout 600;
    proxy_read_timeout 600;
    send_timeout 600;
}

# Static files (frontend)
location /dzirvideo/static/ {
    alias /opt/rag-dz/apps/dzirvideo/public/;
    expires 7d;
    add_header Cache-Control "public, immutable";
}
```

Reload Nginx:
```bash
nginx -t && systemctl reload nginx
```

### 7. Test Public Access

```bash
# From local machine
curl https://iafactory.pro/dzirvideo/health

# Test generator list
curl https://iafactory.pro/dzirvideo/api/v1/generators/list
```

## 🔧 Configuration Details

### Environment Variables Priority

1. **FREE TIER (No API keys needed)**:
   - `DIGEN_SORA`: Completely free, unlimited
   - `COGVIDEO`: Open source (self-hosted)
   - `OPEN_SORA`: Open source (self-hosted)

2. **FREEMIUM (Free tier available)**:
   - `ALIBABA_DASHSCOPE_API_KEY`: WAN 2.1 + Qwen 2.1 (100 videos/day FREE)
   - `KLING_AI_API_KEY`: 66 credits/day (≈10 videos)
   - `PIKA_LABS_API_KEY`: 250 free credits
   - `REPLICATE_API_TOKEN`: $0.002/sec (many generators)

3. **PREMIUM (Paid only)**:
   - `RUNWAY_API_KEY`: Gen-4 ($0.05/sec)
   - `OPENAI_API_KEY`: Sora, DALL-E 3
   - `TOGETHER_API_KEY`: FLUX.1

### Recommended Starter Config

For testing with **ZERO cost**:

```bash
# .env minimal (100% gratuit)
ALIBABA_DASHSCOPE_API_KEY=sk-xxx  # Get from dashscope.console.aliyun.com
YOUTUBE_CLIENT_ID=xxx
YOUTUBE_CLIENT_SECRET=xxx
YOUTUBE_REFRESH_TOKEN=xxx

FREE_ONLY_MODE=true
DEFAULT_GENERATOR=wan_2_1
MAX_BUDGET_PER_VIDEO=0.0
```

This gives you:
- **WAN 2.1** (Alibaba): 100 videos/day, quality 85/100
- **Qwen 2.1** (Alibaba): Unlimited script optimization
- **DIGEN Sora**: Unlimited backup video generator

## 🐳 Docker Compose Configuration

The `docker-compose.yml` includes:

```yaml
services:
  dzirvideo:
    build: .
    container_name: dzir-ia-video
    ports:
      - "8200:8200"
    volumes:
      - ./output:/app/output  # Generated videos
      - ./models:/app/models  # TTS models cache
      - ./config:/app/config  # Generator configs
      - ./.env:/app/.env
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    networks:
      - rag-dz-network
```

### Volume Mounts

- `./output`: All generated videos (audio, subtitles, final videos)
- `./models`: Coqui TTS models (cached after first run)
- `./config`: Optional YAML configs for generators

## 📊 Monitoring & Logs

### View Logs

```bash
# Real-time logs
docker compose logs -f dzirvideo

# Last 100 lines
docker compose logs --tail=100 dzirvideo

# Filter errors only
docker compose logs dzirvideo | grep ERROR
```

### Health Checks

```bash
# Container health
docker ps | grep dzir-ia-video

# API health endpoint
curl http://localhost:8200/health

# Generator status
curl http://localhost:8200/api/v1/generators/status
```

### Metrics Endpoint

```bash
# Request count, latency, errors
curl http://localhost:8200/metrics
```

Returns:
```json
{
  "total_requests": 1234,
  "total_videos_generated": 567,
  "avg_generation_time_seconds": 145.3,
  "generators_used": {
    "wan_2_1": 400,
    "kling_ai": 100,
    "runway_gen4": 67
  },
  "total_cost_usd": 34.50,
  "uptime_seconds": 86400
}
```

## 🔄 Updates & Rollbacks

### Update to New Version

```bash
# From local machine
cd d:\IAFactory\rag-dz\apps\dzirvideo

# Pull latest code
git pull

# Deploy
bash deploy-to-vps.sh

# Or manual on VPS:
ssh root@46.224.3.125
cd /opt/rag-dz/apps/dzirvideo
git pull
docker compose build
docker compose up -d
```

### Rollback

```bash
# On VPS
cd /opt/rag-dz/apps/dzirvideo

# Use previous image
docker compose down
docker images | grep dzir-ia-video  # Find previous tag
docker tag dzir-ia-video:previous dzir-ia-video:latest
docker compose up -d
```

## 🛡️ Security Best Practices

1. **API Keys**: Never commit `.env` to git
2. **Nginx**: Use rate limiting for public endpoints
3. **Firewall**: Only expose port 80/443, block 8200 externally
4. **HTTPS**: Always use SSL (Let's Encrypt)
5. **Secrets**: Rotate API keys every 90 days

### Nginx Rate Limiting

Add to Nginx config:
```nginx
limit_req_zone $binary_remote_addr zone=dzirvideo:10m rate=10r/m;

location /dzirvideo/ {
    limit_req zone=dzirvideo burst=5 nodelay;
    # ... rest of config
}
```

## 🐛 Troubleshooting

### Build Fails with Timeout

```bash
# Increase Docker timeout
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain
docker compose build --no-cache
```

### Container Exits Immediately

```bash
# Check logs for errors
docker compose logs dzirvideo

# Common issues:
# - Missing .env file → cp .env.example .env
# - Invalid API key → check ALIBABA_DASHSCOPE_API_KEY format
# - Port conflict → change API_PORT in .env
```

### Health Check Fails

```bash
# Check if API is listening
docker compose exec dzirvideo netstat -tlnp | grep 8200

# Check application logs
docker compose logs dzirvideo | tail -50

# Test internal endpoint
docker compose exec dzirvideo curl localhost:8200/health
```

### Video Generation Hangs

```bash
# Check generator status
curl http://localhost:8200/api/v1/generators/status

# Check for quota exceeded
docker compose logs dzirvideo | grep "QuotaExceeded"

# Solution: Switch to different generator or wait for quota reset
```

### Out of Disk Space

```bash
# Clean old videos (keep last 7 days)
find /opt/rag-dz/apps/dzirvideo/output -type f -mtime +7 -delete

# Clean Docker images
docker system prune -a --volumes
```

## 📈 Scaling

### Horizontal Scaling (Multiple Instances)

```yaml
# docker-compose.yml
services:
  dzirvideo:
    deploy:
      replicas: 3  # 3 instances
    # ... rest of config

  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    ports:
      - "8200:8200"
```

Nginx load balancer config:
```nginx
upstream dzirvideo_backend {
    least_conn;
    server dzirvideo_1:8200;
    server dzirvideo_2:8200;
    server dzirvideo_3:8200;
}

server {
    listen 8200;
    location / {
        proxy_pass http://dzirvideo_backend;
    }
}
```

### Vertical Scaling (More Resources)

```yaml
# docker-compose.yml
services:
  dzirvideo:
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
```

## 🎯 Production Checklist

Before going live:

- [ ] All required API keys configured in `.env`
- [ ] YouTube OAuth refresh token valid
- [ ] Docker containers healthy (`docker ps`)
- [ ] Health endpoint returns 200 (`curl /health`)
- [ ] Nginx reverse proxy configured
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Rate limiting enabled
- [ ] Firewall rules configured (block 8200)
- [ ] Monitoring enabled (logs, metrics)
- [ ] Backup strategy for output videos
- [ ] Disk space monitored (alert at 80%)
- [ ] Test video generation with free generators
- [ ] Test YouTube upload works
- [ ] Documentation updated

## 📞 Support

- **Issues**: https://github.com/IAFactory/dzirvideo/issues
- **Logs**: Check `docker compose logs dzirvideo`
- **API Docs**: https://iafactory.pro/dzirvideo/docs

---

**Version**: 2.1.0
**Last Updated**: 2025-12-13
**Maintainer**: IAFactory Team
