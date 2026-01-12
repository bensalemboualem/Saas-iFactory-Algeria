# 📚 Complete Deployment Guide - IAFactory Academy

Complete step-by-step guide for deploying IAFactory Academy to production with SSL, monitoring, and backups.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture)
3. [Infrastructure Setup](#infrastructure)
4. [Database Migration](#database)
5. [Application Deployment](#deployment)
6. [SSL/TLS Configuration](#ssl)
7. [Monitoring & Logs](#monitoring)
8. [Backup Strategy](#backups)
9. [Scaling](#scaling)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Ubuntu 22.04 LTS (minimum 2 vCPU, 4GB RAM)
- Docker 20.10+
- Docker Compose 2.0+
- Git
- OpenSSL
- curl

### Domain & DNS
- Valid domain name (e.g., academy.com)
- DNS control access
- SSL certificate (Let's Encrypt - free)

### External Services (Optional but Recommended)
- Stripe account (payments)
- SendGrid account (emails)
- AWS S3 access (backups)
- Sentry account (error tracking)

### Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/iafactory-academy.git
cd iafactory-academy

# Create environment file
cp .env.production.example .env

# Generate secrets
openssl rand -hex 32  # SECRET_KEY
openssl rand -hex 32  # JWT_SECRET
```

---

## Architecture Overview

### Production Stack

```
┌─────────────────────────────────────────────────────────┐
│                     INTERNET                             │
│                       (Users)                             │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │    CloudFlare DNS (Optional)  │
         │  - DDoS Protection            │
         │  - Global Cache               │
         │  - SSL Termination (Optional) │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────────────────────┐
         │         Nginx Reverse Proxy                   │
         │  - SSL/TLS Termination                        │
         │  - Rate Limiting (10 req/s)                   │
         │  - Request Compression (gzip)                 │
         │  - Cache Management                           │
         │  - Security Headers                           │
         └───────────────┬───────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼─────┐                    ┌───▼────┐
    │ Frontend  │                    │ Backend│
    │  React   │                    │FastAPI │
    │  :3000   │                    │ :8000  │
    └────┬─────┘                    └───┬────┘
         │                               │
         │            ┌──────────────────┴──────────────┐
         │            │                                 │
    ┌────▼────────────▼────┐                    ┌──────▼──────┐
    │    PostgreSQL 16     │                    │  Redis 7    │
    │   - Users data       │                    │  - Cache    │
    │   - Courses          │                    │  - Sessions │
    │   - Enrollments      │                    │  - Tokens   │
    │   - Payments         │                    │  - Queues   │
    │   - Certificates     │                    │             │
    └──────────────────────┘                    └─────────────┘
```

### Data Flow
1. User requests → Nginx reverse proxy
2. Nginx handles SSL/TLS, rate limiting, caching
3. Requests routed to Frontend (React SPA) or Backend (FastAPI API)
4. Backend queries PostgreSQL database
5. Cache hits served from Redis
6. Responses compressed and sent to user

---

## Infrastructure Setup

### Step 1: VPS Selection & Creation

#### Option A: Hetzner Cloud (Recommended - 6€/month)

```bash
# 1. Create account: https://www.hetzner.cloud
# 2. Create project
# 3. Create server:
#    - Type: CX21 (2 vCPU, 4GB RAM)
#    - OS: Ubuntu 22.04 LTS
#    - Location: EU (Frankfurt)
#    - SSH Key: Add your public key

# 4. SSH to server
ssh root@YOUR_SERVER_IP

# 5. Update system
apt-get update && apt-get upgrade -y
apt-get install -y curl wget git nano
```

#### Option B: DigitalOcean (5€/month)

```bash
# Create Basic Droplet
# - 2GB Memory
# - 1 vCPU
# - Ubuntu 22.04 x64
# - Add SSH key
```

#### Option C: Linode (5€/month)

```bash
# Create Linode
# - 2GB Plan
# - Ubuntu 22.04 LTS
# - Your region
```

### Step 2: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Add current user to docker group
usermod -aG docker $USER

# Install Docker Compose v2
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 3: Upload Application

```bash
# From your local machine
scp -r . root@YOUR_SERVER_IP:/opt/iafactory-academy

# SSH into server
ssh root@YOUR_SERVER_IP

# Navigate to app directory
cd /opt/iafactory-academy

# Create necessary directories
mkdir -p data/postgres data/redis logs
chmod 755 scripts/*.sh
```

### Step 4: Firewall Configuration

```bash
# Enable UFW firewall
ufw enable

# Allow SSH
ufw allow 22/tcp

# Allow HTTP
ufw allow 80/tcp

# Allow HTTPS
ufw allow 443/tcp

# Verify
ufw status
```

---

## Database Migration

### Step 1: Initialize Database

```bash
# Start PostgreSQL container
docker-compose -f docker-compose.prod.yml up -d db

# Wait for database to be ready
sleep 10

# Verify PostgreSQL is running
docker-compose -f docker-compose.prod.yml logs db | grep "ready to accept"
```

### Step 2: Configure Environment

```bash
# Edit .env file
nano .env

# Make sure these are set:
# POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD
# DATABASE_URL=postgresql://iafactory:PASSWORD@db:5432/iafactory
```

### Step 3: Run Migrations

```bash
# Start API container
docker-compose -f docker-compose.prod.yml up -d api

# Wait for API to start
sleep 5

# Run Alembic migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Verify migration success
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory -c "
  SELECT table_name 
  FROM information_schema.tables 
  WHERE table_schema='public'
"
```

### Step 4: Create Admin User

```bash
# SSH into API container
docker-compose -f docker-compose.prod.yml exec api python

# Python interactive shell
from app.models.user import User
from app.core.database import SessionLocal
from app.core.security import get_password_hash

db = SessionLocal()
admin_user = User(
    email="admin@yourdomain.com",
    hashed_password=get_password_hash("SECURE_PASSWORD_HERE"),
    first_name="Admin",
    last_name="User",
    role="admin",
    is_active=True
)
db.add(admin_user)
db.commit()
print("✅ Admin user created!")
exit()
```

---

## Application Deployment

### Step 1: Build and Start Services

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Verify all services are running
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 2: Health Checks

```bash
# Check backend API
curl http://localhost:8000/health
# Response: {"status":"healthy"}

# Check frontend
curl http://localhost:3000
# Response: HTML content

# Check database
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory -c "SELECT 1"

# Check Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
# Response: PONG
```

### Step 3: Verify Application

```bash
# Test API endpoint
curl -X GET http://localhost:8000/api/v1/courses \
  -H "Accept: application/json"

# Test authentication
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","password":"PASSWORD"}'

# Test database connection
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory -c "
  SELECT COUNT(*) as user_count FROM users;
"
```

---

## SSL/TLS Configuration

### Step 1: DNS Configuration

```bash
# Point your domain to server IP

# In your DNS provider (Cloudflare, GoDaddy, etc):
# A Record: @ → YOUR_SERVER_IP
# A Record: www → YOUR_SERVER_IP
# CNAME Record: api → @ (optional)

# Wait for DNS propagation (5-15 minutes)
nslookup yourdomain.com
```

### Step 2: Install Certbot

```bash
# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Test renewal (dry-run)
certbot renew --dry-run
```

### Step 3: Obtain SSL Certificate

```bash
# Create certificate for your domain
certbot certonly --nginx \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --non-interactive \
  --agree-tos \
  --email admin@yourdomain.com

# Certificate stored in:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Step 4: Update Nginx Configuration

```bash
# Edit nginx configuration
nano deploy/nginx/iafactory.conf

# Update server_name and SSL paths:
# server_name yourdomain.com www.yourdomain.com;
# ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

# Restart Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Step 5: Auto-Renewal

```bash
# Enable certbot auto-renewal
systemctl enable certbot.timer
systemctl start certbot.timer

# Check renewal schedule
systemctl status certbot.timer

# Check certificates
certbot certificates
```

### Step 6: Verify HTTPS

```bash
# Test HTTPS
curl -I https://yourdomain.com
# Response: HTTP/2 200

# Check SSL certificate
curl -vI https://yourdomain.com 2>&1 | grep "SSL"

# Test with SSL Labs
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
```

---

## Monitoring & Logs

### Step 1: View Application Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f db
docker-compose -f docker-compose.prod.yml logs -f redis

# With timestamps
docker-compose -f docker-compose.prod.yml logs -f --timestamps

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs -f --tail 100
```

### Step 2: Monitor System Resources

```bash
# Run monitoring script
./scripts/monitor.sh

# Or manually:
# CPU usage
top -bn1 | grep "Cpu(s)"

# Memory usage
free -h

# Disk usage
df -h /

# Network traffic
iftop
```

### Step 3: Database Monitoring

```bash
# Connect to database
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory

# Check database size
SELECT pg_size_pretty(pg_database_size('iafactory'));

# Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

# Check active connections
SELECT count(*) FROM pg_stat_activity;

# Check slow queries
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

### Step 4: Redis Monitoring

```bash
# Connect to Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli

# Check memory usage
INFO memory

# Check command stats
INFO stats

# Monitor in real-time
MONITOR

# Check connected clients
INFO clients
```

### Step 5: Setup Sentry (Optional)

```bash
# Get Sentry DSN from https://sentry.io

# Add to .env
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# Restart API
docker-compose -f docker-compose.prod.yml restart api

# Errors will now be tracked in Sentry
```

---

## Backup Strategy

### Step 1: Automatic Backups

```bash
# Make script executable
chmod +x scripts/backup.sh

# Run backup
./scripts/backup.sh

# Output:
# backup_20250115_023045.tar.gz

# Schedule daily backups (cron)
# 0 2 * * * cd /opt/iafactory-academy && ./scripts/backup.sh
```

### Step 2: Upload to S3 (Optional)

```bash
# Install AWS CLI
apt-get install -y awscli

# Configure AWS credentials
aws configure
# Access Key: YOUR_KEY
# Secret Key: YOUR_SECRET
# Region: eu-west-1

# Edit backup.sh to include S3 upload:
# aws s3 cp $BACKUP_FILE s3://iafactory-backups/
```

### Step 3: Verify Backups

```bash
# List backups
ls -lh backups/

# Check backup file
tar -tzf backups/backup_*.tar.gz | head

# Backup size
du -h backups/backup_*.tar.gz
```

### Step 4: Restore from Backup

```bash
# Restore from backup file
./scripts/restore.sh backups/backup_20250115_023045.tar.gz

# The script will:
# 1. Backup current data
# 2. Stop services
# 3. Restore PostgreSQL
# 4. Restore Redis
# 5. Start services
# 6. Run migrations
```

---

## Scaling

### Horizontal Scaling (Multiple Servers)

```yaml
# Load Balancer (Nginx/HAProxy)
Load Balancer
    ├── API Server 1
    ├── API Server 2
    └── API Server 3

Shared Resources
    ├── PostgreSQL (RDS)
    └── Redis (ElastiCache)
```

### Vertical Scaling (Bigger Server)

```bash
# Upgrade VPS plan
# CX21 (2vCPU, 4GB) → CX31 (2vCPU, 8GB) → CX41 (4vCPU, 16GB)

# Update docker-compose with more resources:
# services:
#   api:
#     deploy:
#       resources:
#         limits:
#           cpus: '2'
#           memory: 4G

# Restart services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs api

# Rebuild image
docker-compose -f docker-compose.prod.yml build --no-cache

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Force restart
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### Database Connection Error

```bash
# Check PostgreSQL
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory

# Check connection string
echo $DATABASE_URL

# Verify .env
cat .env | grep DATABASE_URL

# Reset database
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

### Port Already in Use

```bash
# Check what's using port 80/443
sudo lsof -i :80
sudo lsof -i :443

# Kill process
sudo kill -9 PID

# Change port in docker-compose.prod.yml if needed
```

### High Memory Usage

```bash
# Check memory
free -h

# Check Docker memory usage
docker stats

# Clean up unused images
docker image prune -a

# Reduce cache size (in nginx.conf)
# proxy_cache_path levels=1:2 keys_zone=api_cache:5m max_size=50m
```

### High Disk Usage

```bash
# Check disk
df -h

# Remove old backups
find backups/ -name "backup_*.tar.gz" -mtime +30 -delete

# Cleanup Docker
docker system prune

# Check logs
du -sh /var/log/*
```

---

## Performance Optimization

### Database Optimization

```bash
# Check index usage
docker-compose -f docker-compose.prod.yml exec db psql -U iafactory << EOF
SELECT schemaname, tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public';
EOF

# Analyze query plans
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

# Vacuum and analyze
VACUUM ANALYZE;
```

### Cache Configuration

```bash
# Redis memory optimization
CONFIG SET maxmemory-policy allkeys-lru

# Nginx cache clearing
docker-compose -f docker-compose.prod.yml exec nginx rm -rf /var/cache/nginx/*
```

### API Optimization

```bash
# Update FastAPI workers
# gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Update in docker-compose.prod.yml:
# command: gunicorn app.main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker
```

---

## Security Best Practices

### 1. Secrets Management

```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Use environment variables for secrets
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET=$(openssl rand -hex 32)

# Rotate secrets regularly
# - Every 90 days for JWT_SECRET
# - Every 6 months for SECRET_KEY
```

### 2. Database Security

```bash
# Use strong passwords
# POSTGRES_PASSWORD: 32 characters, mixed case, numbers, symbols

# Restrict database access
# Only allow connections from API container
# Use network isolation (Docker networks)

# Regular backups
# Daily backups stored securely
# Test restore process monthly
```

### 3. SSL/TLS Security

```bash
# Use strong SSL protocols
ssl_protocols TLSv1.2 TLSv1.3;

# Use strong ciphers
ssl_ciphers HIGH:!aNULL:!MD5;

# Enable HSTS
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### 4. Rate Limiting

```nginx
# General endpoints: 10 req/s
# API endpoints: 30 req/s
# Login: 5 req/minute
# Upload: 1 req/second
```

### 5. Security Headers

```bash
# X-Frame-Options: SAMEORIGIN
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Content-Security-Policy: ...
# Referrer-Policy: strict-origin-when-cross-origin
```

---

## Support & Resources

### Logs and Debugging

```bash
# Application logs
docker-compose -f docker-compose.prod.yml logs -f api

# Database logs
docker-compose -f docker-compose.prod.yml logs -f db

# Nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx

# System logs
journalctl -u docker -f
```

### Documentation

- FastAPI: https://fastapi.tiangolo.com
- React: https://react.dev
- PostgreSQL: https://www.postgresql.org/docs
- Docker: https://docs.docker.com
- Nginx: https://nginx.org/en/docs

### Getting Help

- Check logs: `docker-compose logs -f`
- Check health: `curl http://localhost:8000/health`
- Monitor: `./scripts/monitor.sh`
- Read documentation: `./docs`

---

**Deployment Complete! 🚀**

Your IAFactory Academy is now running in production!

For updates and patches, see the CI/CD section in the deployment guide.
