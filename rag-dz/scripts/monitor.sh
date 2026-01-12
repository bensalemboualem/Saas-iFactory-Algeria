#!/bin/bash
# Monitoring continu IAFactory

watch -n 5 'clear && echo "=== IAFACTORY MONITORING ===" && \
echo "" && \
echo "Backend Status:" && \
ssh root@46.224.3.125 "curl -s http://localhost:8180/health | python3 -m json.tool" && \
echo "" && \
echo "Providers Actifs:" && \
ssh root@46.224.3.125 "curl -s http://localhost:8180/api/credentials/ | python3 -m json.tool | grep -E \"(provider|has_key)\" | paste - - | grep true | wc -l" && \
echo "" && \
echo "Docker Containers:" && \
ssh root@46.224.3.125 "docker ps --format \"table {{.Names}}\t{{.Status}}\" | grep iaf" && \
echo "" && \
echo "Dernières requêtes API:" && \
ssh root@46.224.3.125 "docker logs iaf-backend-prod --tail 5 | grep INFO"'
