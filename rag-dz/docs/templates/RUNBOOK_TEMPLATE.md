# [Service/Module] Runbook

**Service**: [Service Name]
**Owner**: [Team Name]
**On-Call**: [Contact/Slack Channel]
**Last Updated**: [YYYY-MM-DD]

---

## 🎯 Service Overview

### Purpose
[Brief description of service function]

### Key Metrics
- **Uptime SLA**: 99.9%
- **Response Time (p95)**: < 200ms
- **Error Rate**: < 0.1%

### Dependencies
- PostgreSQL (critical)
- Redis (critical)
- External API (non-critical)

---

## 🚨 Common Issues & Solutions

### Issue 1: Service Not Responding

**Symptoms**:
- Health check returning 503
- Container restarting repeatedly
- High error rate in logs

**Diagnosis**:
```bash
# Check container status
docker ps -a | grep [service-name]

# View recent logs
docker logs --tail 100 [container-name]

# Check resource usage
docker stats [container-name]
```

**Resolution**:
```bash
# Restart service
docker-compose restart [service-name]

# If restart fails, rebuild
docker-compose up -d --force-recreate [service-name]

# Check health
curl http://localhost:[port]/health
```

**Escalation**: If issue persists after 2 restarts, contact [Lead Developer]

---

### Issue 2: Database Connection Errors

**Symptoms**:
- `psycopg2.OperationalError` in logs
- Requests timing out
- "Connection pool exhausted" errors

**Diagnosis**:
```bash
# Check PostgreSQL status
docker exec iaf-dz-postgres pg_isready -U postgres

# Check connection count
docker exec iaf-dz-postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"

# View active connections
docker exec iaf-dz-postgres psql -U postgres -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

**Resolution**:
```bash
# Option 1: Restart application to clear connection pool
docker-compose restart [service-name]

# Option 2: Restart PostgreSQL (last resort)
docker-compose restart iafactory-postgres

# Option 3: Kill idle connections
docker exec iaf-dz-postgres psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND state_change < NOW() - INTERVAL '5 minutes';"
```

**Prevention**:
- Increase `MAX_CONNECTIONS` in PostgreSQL config
- Tune connection pool settings in application

---

### Issue 3: High Memory Usage

**Symptoms**:
- Container using >2GB RAM
- OOM (Out of Memory) kills
- Slow response times

**Diagnosis**:
```bash
# Check memory usage
docker stats [container-name] --no-stream

# Check Python memory usage (if backend)
docker exec [container-name] python -c "import psutil; print(psutil.virtual_memory())"

# View top processes
docker exec [container-name] top -bn1
```

**Resolution**:
```bash
# Restart to clear memory leaks
docker-compose restart [service-name]

# Increase memory limit in docker-compose.yml
# Add under service definition:
# deploy:
#   resources:
#     limits:
#       memory: 4G

# Apply changes
docker-compose up -d [service-name]
```

**Long-term Fix**: Profile application for memory leaks

---

### Issue 4: External API Timeout

**Symptoms**:
- Requests to [External Service] failing
- `ReadTimeout` errors in logs
- Increased response times

**Diagnosis**:
```bash
# Test external API manually
curl -v -m 10 https://[external-api-endpoint]

# Check network connectivity
docker exec [container-name] ping -c 3 [external-host]

# View error logs
docker logs [container-name] | grep -i "timeout"
```

**Resolution**:
```bash
# Option 1: Increase timeout in config
# Edit .env.local:
# [SERVICE]_TIMEOUT=60

# Reload config
docker-compose up -d [service-name]

# Option 2: Fallback to cached data (if implemented)
# Enable fallback mode in config

# Option 3: Disable feature temporarily
# Set [FEATURE]_ENABLED=false in .env.local
```

**Escalation**: Contact external API provider if persistent

---

## 🔄 Routine Operations

### Starting Services
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d [service-name]

# Start with logs visible
docker-compose up [service-name]
```

### Stopping Services
```bash
# Stop all services
docker-compose down

# Stop specific service
docker-compose stop [service-name]

# Stop and remove volumes (⚠️ DATA LOSS)
docker-compose down -v
```

### Viewing Logs
```bash
# Follow logs
docker-compose logs -f [service-name]

# Last 100 lines
docker logs --tail 100 [container-name]

# Logs with timestamps
docker logs --timestamps [container-name]

# Logs for specific time range
docker logs --since 2024-11-24T10:00:00 [container-name]
```

### Scaling Services
```bash
# Scale to 3 replicas
docker-compose up -d --scale [service-name]=3

# Verify scaling
docker ps | grep [service-name]
```

---

## 💾 Backup & Recovery

### Database Backup
```bash
# Create backup
./scripts/db-backup.sh backup_manual_$(date +%Y%m%d)

# Verify backup
ls -lh backups/

# Backups are stored in: ./backups/
```

### Database Restore
```bash
# ⚠️ WARNING: This will overwrite current database

# Stop application services
docker-compose stop iafactory-backend iafactory-hub iafactory-docs

# Restore from backup
gunzip < backups/[backup-name].sql.gz | \
  docker exec -i iaf-dz-postgres psql -U postgres iafactory_dz

# Restart services
docker-compose start iafactory-backend iafactory-hub iafactory-docs

# Verify data
docker exec iaf-dz-postgres psql -U postgres -d iafactory_dz -c "SELECT COUNT(*) FROM [table_name];"
```

---

## 📊 Health Checks

### Automated Health Check
```bash
./scripts/health-check.sh
```

### Manual Health Checks
```bash
# Backend API
curl http://localhost:8180/health

# Frontend Hub
curl http://localhost:8182

# PostgreSQL
docker exec iaf-dz-postgres pg_isready -U postgres

# Redis
docker exec iaf-dz-redis redis-cli ping

# Qdrant
curl http://localhost:6332/healthz
```

---

## 🔍 Debugging Tips

### Enable Debug Logging
```bash
# Edit .env.local
LOG_LEVEL=DEBUG

# Restart service
docker-compose restart [service-name]

# View debug logs
docker logs -f [container-name]
```

### Access Container Shell
```bash
# Bash shell (if available)
docker exec -it [container-name] /bin/bash

# Sh shell (Alpine images)
docker exec -it [container-name] /bin/sh

# Python interactive shell (backend)
docker exec -it iaf-dz-backend python
```

### Inspect Database
```bash
# PostgreSQL shell
docker exec -it iaf-dz-postgres psql -U postgres iafactory_dz

# List tables
\dt

# Describe table
\d [table_name]

# Run query
SELECT * FROM [table_name] LIMIT 10;
```

---

## 📞 Escalation

### Level 1: On-Call Engineer
- **Contact**: [Slack Channel / Phone]
- **Response Time**: 15 minutes
- **Scope**: Common issues, restarts, basic troubleshooting

### Level 2: Lead Developer
- **Contact**: [Email / Phone]
- **Response Time**: 1 hour
- **Scope**: Code issues, complex debugging, architecture questions

### Level 3: CTO / Architect
- **Contact**: [Email / Phone]
- **Response Time**: 4 hours
- **Scope**: System-wide failures, architectural decisions

---

## 📚 Additional Resources

- **Monitoring Dashboard**: [Grafana Link]
- **Error Tracking**: [Sentry Link]
- **Documentation**: [Confluence/Notion Link]
- **CI/CD Pipeline**: [GitHub Actions Link]
