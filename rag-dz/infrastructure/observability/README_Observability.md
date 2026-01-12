# Module 9 : Monitoring & Observabilité - iaFactoryDZ

## 📊 Vue d'ensemble

Stack complète de monitoring pour les ~30 containers iaFactory sur VPS Hetzner CX43.

| Composant | Port | Description |
|-----------|------|-------------|
| **Grafana** | 3033 | Dashboards et visualisation |
| **Prometheus** | 9090 | Base de métriques time-series |
| **Loki** | 3100 | Agrégation de logs |
| **Promtail** | - | Collecteur de logs Docker |
| **cAdvisor** | 8888 | Métriques containers |
| **Node Exporter** | 9100 | Métriques système (CPU, RAM, Disk) |
| **Alertmanager** | 9093 | Gestion des alertes |

---

## 🌐 URLs d'accès

### Grafana Dashboard
```
https://www.iafactoryalgeria.com/grafana/
```
- **User**: admin
- **Password**: iaFactoryDZ2024!

### Prometheus (protégé Basic Auth)
```
https://www.iafactoryalgeria.com/prometheus/
```
- **User**: iafadmin
- **Password**: iaFactoryDZ2024!

### Alertmanager (protégé Basic Auth)
```
https://www.iafactoryalgeria.com/alertmanager/
```
- **User**: iafadmin
- **Password**: iaFactoryDZ2024!

---

## 📁 Structure des fichiers

```
/opt/observability/
├── docker-compose.observability.yml   # Stack complète
├── prometheus.yml                     # Config scraping Prometheus
├── loki-config.yml                    # Config Loki
├── promtail-config.yml                # Config collecteur logs
├── alert.rules.yml                    # Règles d'alertes
├── alertmanager.yml                   # Config notifications
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── datasources.yml        # Sources Prometheus + Loki
        └── dashboards/
            └── dashboards.yml         # Auto-provision dashboards
```

---

## 🚀 Commandes de gestion

### Démarrer/Arrêter la stack
```bash
cd /opt/observability
docker-compose -f docker-compose.observability.yml up -d
docker-compose -f docker-compose.observability.yml down
```

### Grafana (lancé manuellement)
```bash
# Démarrer Grafana
docker run -d \
  --name iaf-grafana \
  --network observability_observability_net \
  -p 3033:3000 \
  -e GF_SECURITY_ADMIN_USER=admin \
  -e GF_SECURITY_ADMIN_PASSWORD=iaFactoryDZ2024! \
  -e GF_USERS_ALLOW_SIGN_UP=false \
  -e GF_SERVER_ROOT_URL=https://www.iafactoryalgeria.com/grafana/ \
  -e GF_SERVER_SERVE_FROM_SUB_PATH=true \
  -v grafana-data:/var/lib/grafana \
  -v /opt/observability/grafana/provisioning:/etc/grafana/provisioning \
  --restart unless-stopped \
  grafana/grafana:10.2.2

# Arrêter Grafana
docker stop iaf-grafana && docker rm iaf-grafana
```

### Voir les logs
```bash
docker logs -f iaf-prometheus
docker logs -f iaf-grafana
docker logs -f iaf-loki
docker logs -f iaf-promtail
```

### Vérifier la santé
```bash
# Prometheus
curl http://127.0.0.1:9090/-/healthy

# Grafana
curl http://127.0.0.1:3033/api/health

# Loki
curl http://127.0.0.1:3100/ready

# cAdvisor
curl http://127.0.0.1:8888/healthz
```

---

## 📈 Métriques collectées

### Via Node Exporter (système)
- CPU usage (%)
- Memory usage (%)
- Disk I/O
- Network bandwidth
- Filesystem usage

### Via cAdvisor (containers)
- Container CPU
- Container Memory
- Container Network I/O
- Container restarts

### Via Prometheus scraping (apps)
- Targets: ports 8180-8207
- Endpoints: /metrics ou /health
- Intervalle: 15s

---

## 🔔 Alertes configurées

| Alerte | Condition | Sévérité |
|--------|-----------|----------|
| HighCPU | CPU > 80% pendant 5min | critical |
| HighMemory | RAM > 85% pendant 5min | critical |
| DiskAlmostFull | Disk > 85% | critical |
| ContainerRestarting | > 3 restarts en 10min | warning |
| ContainerDown | Container arrêté > 1min | critical |
| ServiceDown | Service HTTP down > 2min | critical |

---

## 🎛️ Dashboards Grafana recommandés

Importez ces dashboards (Grafana > + > Import) :

| Dashboard | ID | Description |
|-----------|-----|-------------|
| Node Exporter Full | 1860 | Métriques système détaillées |
| Docker Container | 893 | Vue containers |
| cAdvisor | 14282 | Métriques cAdvisor |
| Loki Logs | 13639 | Exploration logs |

---

## 🔧 Troubleshooting

### Prometheus ne scrape pas les cibles
```bash
# Vérifier targets
curl http://127.0.0.1:9090/api/v1/targets | jq
```

### Logs non visibles dans Loki
```bash
# Vérifier Promtail
docker logs iaf-promtail

# Tester query Loki
curl -G -s "http://127.0.0.1:3100/loki/api/v1/labels"
```

### Grafana ne démarre pas
```bash
# Vérifier permissions
docker exec iaf-grafana ls -la /var/lib/grafana

# Recréer volume
docker volume rm grafana-data
```

---

## 📅 Rétention des données

| Service | Rétention |
|---------|-----------|
| Prometheus | 15 jours |
| Loki | 31 jours (744h) |
| Grafana | Permanent (dashboards) |

---

## 🔐 Sécurité

- **Grafana**: Authentification interne (admin)
- **Prometheus/Alertmanager**: Basic Auth nginx
- **Ports**: Tous les ports exposés uniquement sur localhost (127.0.0.1)
- **htpasswd**: `/etc/nginx/.htpasswd_monitoring`

---

## 📋 Résumé déploiement Module 9

✅ **Composants déployés:**
- 7 containers observabilité fonctionnels
- Prometheus scraping 30+ containers
- Grafana avec datasources auto-provisionnées
- Loki + Promtail pour logs centralisés
- Alertes configurées (CPU, RAM, Disk, Containers)
- Routes nginx sécurisées (Basic Auth)

✅ **Validation:**
```bash
# Stack complète
docker ps --filter "name=iaf-" | grep -E "grafana|prometheus|loki|promtail|cadvisor|node-exporter|alertmanager"

# Health checks
curl http://127.0.0.1:9090/-/healthy   # Prometheus
curl http://127.0.0.1:3033/api/health  # Grafana
curl http://127.0.0.1:3100/ready       # Loki
```

---

**Date de déploiement**: Novembre 2025  
**VPS**: 46.224.3.125 (Hetzner CX43)  
**Domaine**: www.iafactoryalgeria.com
