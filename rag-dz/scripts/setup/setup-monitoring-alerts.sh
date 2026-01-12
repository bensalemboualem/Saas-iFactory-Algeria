#!/bin/bash
# ================================================================
# CONFIGURATION ALERTES MONITORING
# IAFactory Algeria - Prometheus + AlertManager
# ================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "================================================================"
echo "🔔 CONFIGURATION ALERTES MONITORING"
echo "================================================================"
echo ""

# ================================================================
# CONFIGURATION
# ================================================================

PROMETHEUS_DIR="/opt/iafactory-rag-dz/monitoring/prometheus"
ALERTMANAGER_DIR="/opt/iafactory-rag-dz/monitoring/alertmanager"
ALERTS_FILE="$PROMETHEUS_DIR/alerts.yml"
ALERTMANAGER_CONFIG="$ALERTMANAGER_DIR/alertmanager.yml"

echo "Configuration:"
echo "  • Prometheus config: $PROMETHEUS_DIR"
echo "  • AlertManager config: $ALERTMANAGER_DIR"
echo ""

# ================================================================
# ÉTAPE 1: CRÉATION STRUCTURE
# ================================================================

echo -e "${BLUE}[1/5]${NC} Création de la structure..."

mkdir -p "$PROMETHEUS_DIR"
mkdir -p "$ALERTMANAGER_DIR"

echo -e "${GREEN}✅ Structure créée${NC}"
echo ""

# ================================================================
# ÉTAPE 2: RÈGLES D'ALERTES PROMETHEUS
# ================================================================

echo -e "${BLUE}[2/5]${NC} Création des règles d'alertes Prometheus..."

cat > "$ALERTS_FILE" << 'ALERTSYML'
groups:
  # ================================================================
  # ALERTES INFRASTRUCTURE
  # ================================================================
  - name: infrastructure
    interval: 30s
    rules:
      # Container down
      - alert: ContainerDown
        expr: up{job="docker"} == 0
        for: 2m
        labels:
          severity: critical
          category: infrastructure
        annotations:
          summary: "Container {{ $labels.instance }} down"
          description: "Le container {{ $labels.container_name }} est arrêté depuis 2 minutes"

      # High CPU
      - alert: HighCPUUsage
        expr: (100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)) > 80
        for: 5m
        labels:
          severity: warning
          category: performance
        annotations:
          summary: "CPU élevé sur {{ $labels.instance }}"
          description: "CPU utilisation: {{ $value }}% (seuil: 80%)"

      # High Memory
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 90
        for: 5m
        labels:
          severity: critical
          category: performance
        annotations:
          summary: "Mémoire élevée sur {{ $labels.instance }}"
          description: "RAM utilisation: {{ $value }}% (seuil: 90%)"

      # Low Disk Space
      - alert: LowDiskSpace
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 5m
        labels:
          severity: critical
          category: infrastructure
        annotations:
          summary: "Espace disque faible sur {{ $labels.instance }}"
          description: "Espace libre: {{ $value }}% (seuil: 10%)"

      # High Load Average
      - alert: HighLoadAverage
        expr: node_load15 > 4
        for: 10m
        labels:
          severity: warning
          category: performance
        annotations:
          summary: "Load average élevé sur {{ $labels.instance }}"
          description: "Load average (15min): {{ $value }} (seuil: 4.0)"

  # ================================================================
  # ALERTES CONTAINERS
  # ================================================================
  - name: containers
    interval: 30s
    rules:
      # Container unhealthy
      - alert: ContainerUnhealthy
        expr: container_health_status{health_status!="healthy"} == 1
        for: 3m
        labels:
          severity: warning
          category: containers
        annotations:
          summary: "Container {{ $labels.name }} unhealthy"
          description: "Health status: {{ $labels.health_status }}"

      # Container high memory
      - alert: ContainerHighMemory
        expr: (container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100 > 90
        for: 5m
        labels:
          severity: warning
          category: containers
        annotations:
          summary: "Container {{ $labels.name }} mémoire élevée"
          description: "Utilisation: {{ $value }}%"

      # Container restarts
      - alert: ContainerRestarts
        expr: rate(container_restart_count[15m]) > 0
        for: 5m
        labels:
          severity: warning
          category: containers
        annotations:
          summary: "Container {{ $labels.name }} redémarrages fréquents"
          description: "{{ $value }} restarts dans les 15 dernières minutes"

  # ================================================================
  # ALERTES SERVICES CRITIQUES
  # ================================================================
  - name: critical_services
    interval: 30s
    rules:
      # PostgreSQL down
      - alert: PostgreSQLDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
          category: database
        annotations:
          summary: "PostgreSQL inaccessible"
          description: "La base de données PostgreSQL ne répond pas"

      # Archon down
      - alert: ArchonDown
        expr: up{job="archon"} == 0
        for: 2m
        labels:
          severity: critical
          category: application
        annotations:
          summary: "Archon inaccessible"
          description: "Le service Archon ne répond pas"

      # Ollama down
      - alert: OllamaDown
        expr: up{job="ollama"} == 0
        for: 2m
        labels:
          severity: warning
          category: ai
        annotations:
          summary: "Ollama LLM inaccessible"
          description: "Le service Ollama ne répond pas"

      # Nginx down
      - alert: NginxDown
        expr: up{job="nginx"} == 0
        for: 1m
        labels:
          severity: critical
          category: infrastructure
        annotations:
          summary: "Nginx inaccessible"
          description: "Le reverse proxy Nginx ne répond pas"

  # ================================================================
  # ALERTES BACKUPS
  # ================================================================
  - name: backups
    interval: 1h
    rules:
      # Backup PostgreSQL ancien
      - alert: PostgreSQLBackupOld
        expr: time() - postgres_last_backup_timestamp > 86400
        for: 1h
        labels:
          severity: warning
          category: backup
        annotations:
          summary: "Backup PostgreSQL ancien"
          description: "Dernier backup il y a plus de 24h"

      # Backup échoué
      - alert: BackupFailed
        expr: postgres_backup_success == 0
        for: 5m
        labels:
          severity: critical
          category: backup
        annotations:
          summary: "Backup PostgreSQL échoué"
          description: "Le dernier backup a échoué"

  # ================================================================
  # ALERTES SSL
  # ================================================================
  - name: ssl
    interval: 1d
    rules:
      # Certificat SSL expire bientôt
      - alert: SSLCertificateExpireSoon
        expr: ssl_cert_expiry_days < 30
        for: 1h
        labels:
          severity: warning
          category: security
        annotations:
          summary: "Certificat SSL expire dans {{ $value }} jours"
          description: "Domaine: {{ $labels.domain }}"

      # Certificat SSL expiré
      - alert: SSLCertificateExpired
        expr: ssl_cert_expiry_days < 0
        for: 5m
        labels:
          severity: critical
          category: security
        annotations:
          summary: "Certificat SSL EXPIRÉ"
          description: "Domaine: {{ $labels.domain }}"

  # ================================================================
  # ALERTES APPLICATIVES
  # ================================================================
  - name: applications
    interval: 1m
    rules:
      # HTTP 5xx errors
      - alert: HighHTTP5xxRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
          category: application
        annotations:
          summary: "Taux élevé d'erreurs HTTP 5xx"
          description: "{{ $value }} erreurs/sec sur {{ $labels.service }}"

      # Slow response time
      - alert: SlowResponseTime
        expr: http_request_duration_seconds{quantile="0.99"} > 5
        for: 5m
        labels:
          severity: warning
          category: performance
        annotations:
          summary: "Temps de réponse lent"
          description: "P99: {{ $value }}s (seuil: 5s) sur {{ $labels.service }}"

      # High error rate
      - alert: HighErrorRate
        expr: rate(application_errors_total[5m]) > 10
        for: 5m
        labels:
          severity: warning
          category: application
        annotations:
          summary: "Taux d'erreur élevé"
          description: "{{ $value }} erreurs/sec dans {{ $labels.service }}"
ALERTSYML

echo -e "${GREEN}✅ Règles d'alertes créées: $ALERTS_FILE${NC}"
echo ""

# ================================================================
# ÉTAPE 3: CONFIGURATION ALERTMANAGER
# ================================================================

echo -e "${BLUE}[3/5]${NC} Configuration AlertManager..."

cat > "$ALERTMANAGER_CONFIG" << 'ALERTMGRYML'
global:
  # Configuration globale
  resolve_timeout: 5m
  smtp_smarthost: 'localhost:25'
  smtp_from: 'alertmanager@iafactoryalgeria.com'
  smtp_require_tls: false

# Templates
templates:
  - '/etc/alertmanager/templates/*.tmpl'

# Routes d'alertes
route:
  # Route par défaut
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  # Routes spécifiques par sévérité
  routes:
    # Alertes critiques - notification immédiate
    - match:
        severity: critical
      receiver: 'critical'
      group_wait: 10s
      repeat_interval: 1h

    # Alertes warning - notification groupée
    - match:
        severity: warning
      receiver: 'warning'
      group_wait: 5m
      repeat_interval: 12h

    # Alertes backup
    - match:
        category: backup
      receiver: 'backup-alerts'
      repeat_interval: 24h

    # Alertes sécurité (SSL)
    - match:
        category: security
      receiver: 'security-alerts'
      repeat_interval: 24h

# Receivers (destinations des alertes)
receivers:
  # Receiver par défaut (logs)
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:9099/webhook'
        send_resolved: true

  # Alertes critiques
  - name: 'critical'
    # Email
    email_configs:
      - to: 'admin@iafactoryalgeria.com'
        subject: '🚨 [CRITIQUE] {{ .GroupLabels.alertname }}'
        html: |
          <h2>Alerte Critique IAFactory</h2>
          <p><strong>Alerte:</strong> {{ .GroupLabels.alertname }}</p>
          <p><strong>Sévérité:</strong> {{ .CommonLabels.severity }}</p>
          <p><strong>Description:</strong> {{ .CommonAnnotations.description }}</p>
          <p><strong>Heure:</strong> {{ .StartsAt }}</p>

    # Webhook (optionnel - Slack, Discord, etc.)
    webhook_configs:
      - url: 'http://localhost:9099/webhook/critical'
        send_resolved: true

  # Alertes warning
  - name: 'warning'
    email_configs:
      - to: 'monitoring@iafactoryalgeria.com'
        subject: '⚠️  [WARNING] {{ .GroupLabels.alertname }}'

  # Alertes backup
  - name: 'backup-alerts'
    email_configs:
      - to: 'backup@iafactoryalgeria.com'
        subject: '💾 [BACKUP] {{ .GroupLabels.alertname }}'

  # Alertes sécurité
  - name: 'security-alerts'
    email_configs:
      - to: 'security@iafactoryalgeria.com'
        subject: '🔒 [SECURITY] {{ .GroupLabels.alertname }}'

# Inhibition rules (empêcher certaines alertes si d'autres sont actives)
inhibit_rules:
  # Si un container est down, ne pas alerter sur ses metrics
  - source_match:
      severity: 'critical'
      alertname: 'ContainerDown'
    target_match:
      severity: 'warning'
    equal: ['container_name']

  # Si le serveur est down, ne pas alerter sur les services
  - source_match:
      alertname: 'InstanceDown'
    target_match_re:
      alertname: '(ContainerDown|ServiceDown)'
ALERTMGRYML

echo -e "${GREEN}✅ Configuration AlertManager créée${NC}"
echo ""

# ================================================================
# ÉTAPE 4: MISE À JOUR PROMETHEUS CONFIG
# ================================================================

echo -e "${BLUE}[4/5]${NC} Mise à jour configuration Prometheus..."

PROMETHEUS_CONFIG="$PROMETHEUS_DIR/prometheus.yml"

cat > "$PROMETHEUS_CONFIG" << 'PROMYML'
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'iafactory-algeria'
    environment: 'production'

# Chargement des règles d'alertes
rule_files:
  - '/etc/prometheus/alerts.yml'

# Configuration AlertManager
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - 'iaf-alertmanager:9093'

# Jobs de scraping
scrape_configs:
  # Prometheus lui-même
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter (métriques système)
  - job_name: 'node'
    static_configs:
      - targets: ['iaf-node-exporter:9100']
        labels:
          instance: 'iafactorysuisse'

  # cAdvisor (métriques containers)
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['iaf-cadvisor:8080']

  # Containers Docker (via cAdvisor)
  - job_name: 'docker'
    static_configs:
      - targets: ['iaf-cadvisor:8080']
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 'iaf-cadvisor:8080'

  # PostgreSQL (si exporter installé)
  - job_name: 'postgres'
    static_configs:
      - targets: ['iaf-postgres-exporter:9187']

  # Nginx (si exporter installé)
  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']

  # Applications (à configurer dans chaque app)
  - job_name: 'archon'
    static_configs:
      - targets: ['archon-server:8181']
    metrics_path: '/metrics'

  - job_name: 'backend'
    static_configs:
      - targets: ['iaf-backend-prod:8180']
    metrics_path: '/metrics'
PROMYML

echo -e "${GREEN}✅ Configuration Prometheus mise à jour${NC}"
echo ""

# ================================================================
# ÉTAPE 5: REDÉMARRAGE SERVICES
# ================================================================

echo -e "${BLUE}[5/5]${NC} Redémarrage des services monitoring..."

cd /opt/iafactory-rag-dz

# Vérifier si les containers existent
if docker ps | grep -q "iaf-prometheus"; then
    echo "Redémarrage Prometheus..."
    docker restart iaf-prometheus
    echo -e "${GREEN}✅ Prometheus redémarré${NC}"
fi

if docker ps | grep -q "iaf-alertmanager"; then
    echo "Redémarrage AlertManager..."
    docker restart iaf-alertmanager
    echo -e "${GREEN}✅ AlertManager redémarré${NC}"
fi

echo ""
echo "⏳ Attente 10 secondes..."
sleep 10

# ================================================================
# VÉRIFICATION
# ================================================================

echo ""
echo "📊 Vérification des services..."
echo ""

# Prometheus
if timeout 3 curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅ Prometheus: Healthy${NC}"
else
    echo -e "  ${RED}❌ Prometheus: Non accessible${NC}"
fi

# AlertManager
if timeout 3 curl -s http://localhost:9093/-/healthy > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅ AlertManager: Healthy${NC}"
else
    echo -e "  ${RED}❌ AlertManager: Non accessible${NC}"
fi

# Règles chargées
if timeout 3 curl -s http://localhost:9090/api/v1/rules 2>&1 | grep -q "alerts.yml"; then
    echo -e "  ${GREEN}✅ Règles d'alertes: Chargées${NC}"
else
    echo -e "  ${YELLOW}⚠️  Règles d'alertes: À vérifier${NC}"
fi

echo ""

# ================================================================
# RÉSUMÉ
# ================================================================

echo "================================================================"
echo -e "${GREEN}✅ CONFIGURATION ALERTES TERMINÉE${NC}"
echo "================================================================"
echo ""

echo "📋 RÉSUMÉ:"
echo ""

echo "Fichiers créés:"
echo "  • $ALERTS_FILE"
echo "  • $ALERTMANAGER_CONFIG"
echo "  • $PROMETHEUS_CONFIG"
echo ""

echo "Groupes d'alertes configurés:"
echo "  • Infrastructure (5 alertes)"
echo "  • Containers (3 alertes)"
echo "  • Services critiques (4 alertes)"
echo "  • Backups (2 alertes)"
echo "  • SSL (2 alertes)"
echo "  • Applications (3 alertes)"
echo ""

echo "Receivers configurés:"
echo "  • critical → admin@iafactoryalgeria.com"
echo "  • warning → monitoring@iafactoryalgeria.com"
echo "  • backup → backup@iafactoryalgeria.com"
echo "  • security → security@iafactoryalgeria.com"
echo ""

echo "🌐 INTERFACES:"
echo "  • Prometheus: http://localhost:9090"
echo "  • AlertManager: http://localhost:9093"
echo "  • Grafana: http://localhost:3033"
echo ""

echo "🔧 COMMANDES UTILES:"
echo ""
echo "Voir les alertes actives:"
echo "  curl http://localhost:9090/api/v1/alerts"
echo ""
echo "Tester une règle:"
echo "  curl http://localhost:9090/api/v1/rules"
echo ""
echo "Silencer une alerte (AlertManager UI):"
echo "  http://localhost:9093/#/silences"
echo ""
echo "Logs Prometheus:"
echo "  docker logs iaf-prometheus -f"
echo ""
echo "Logs AlertManager:"
echo "  docker logs iaf-alertmanager -f"
echo ""

echo "📧 CONFIGURATION EMAIL:"
echo "  ⚠️  Pour que les emails fonctionnent, configurez un SMTP:"
echo "  1. Modifier alertmanager.yml"
echo "  2. Ajouter smtp_smarthost, smtp_auth_username, smtp_auth_password"
echo "  3. Redémarrer AlertManager"
echo ""

echo "================================================================"
echo "✅ Monitoring et alertes configurés avec succès!"
echo "================================================================"
echo ""
