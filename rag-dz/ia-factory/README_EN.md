# IA Factory - Complete Content Automation Platform

An AI-powered content automation platform to create, edit, and distribute videos across multiple platforms.

## 🚀 Features

### Phase 1: Brand Configuration
- Brand voice and tone configuration
- Content pillars definition
- Team management with invitations

### Phase 2: Content Generation
- Script generation with Claude AI
- Video creation with VEO 3 (Replicate)
- Automatic editing with FFmpeg
- Smart content calendar

### Phase 3: Multi-Platform Distribution
- Publishing on Instagram, TikTok, YouTube, LinkedIn
- Automatic video format conversion
- Caption and hashtag adaptation
- Publication scheduling

### Phase 4: Analytics & Optimization
- Unified dashboard
- AI recommendations to improve performance
- Automated reports
- Trend detection

## 📋 Prerequisites

- Python 3.11+
- MongoDB 7.0+
- Redis 7+
- FFmpeg
- Docker & Docker Compose (recommended)

## 🛠 Installation

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
cd ia-factory

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 2: Local Installation

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env

# Start MongoDB and Redis (or use cloud services)
# ...

# Start application
uvicorn app.main:app --reload --port 8000
```

## 🔑 Configuration

### Required Environment Variables

```env
# AI Services
ANTHROPIC_API_KEY=sk-ant-...      # Required for script generation
REPLICATE_API_TOKEN=r8_...         # Required for video generation

# Database
MONGODB_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0

# Social platforms (optional)
INSTAGRAM_ACCESS_TOKEN=...
TIKTOK_ACCESS_TOKEN=...
YOUTUBE_CLIENT_ID=...
LINKEDIN_ACCESS_TOKEN=...
```

## 📚 API Documentation

Once the application is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/brand/setup` | Configure a new brand |
| `POST /api/content/generate-scripts` | Generate scripts |
| `POST /api/content/generate-videos` | Create videos |
| `POST /api/content/auto-edit` | Automatically edit |
| `POST /api/distribution/publish` | Publish content |
| `GET /api/analytics/dashboard` | Analytics dashboard |

## 🏗 Architecture

```
ia-factory/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routes
│   │   ├── models/        # Pydantic models
│   │   ├── services/      # Business logic
│   │   ├── tasks/         # Celery tasks
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # MongoDB connection
│   │   └── main.py        # Entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # (Coming soon)
├── docker-compose.yml
└── .env.example
```

## 🔄 Typical Workflow

1. **Initial Setup**
   ```
   POST /api/brand/setup
   {
     "name": "My Brand",
     "industry": "tech",
     "tone": "professional",
     "content_pillars": ["innovation", "tutorials"]
   }
   ```

2. **Script Generation**
   ```
   POST /api/content/generate-scripts
   {
     "brand_id": "...",
     "topic": "Introduction to AI",
     "content_type": "short_video"
   }
   ```

3. **Video Creation**
   ```
   POST /api/content/generate-videos
   {
     "script_id": "...",
     "brand_id": "...",
     "style": "modern"
   }
   ```

4. **Publishing**
   ```
   POST /api/distribution/publish
   {
     "content_id": "...",
     "platforms": ["instagram", "tiktok"]
   }
   ```

## 🧪 Tests

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

## 📈 Monitoring

- Health Check: `GET /health`
- API Status: `GET /api/status`

## 🔒 Security

- All API keys must be stored in environment variables
- Platform credentials are encrypted in the database
- CORS configured for production

## 📝 License

MIT License

## 🤝 Support

For any questions or support, contact the IA Factory team.
