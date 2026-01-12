# 🔐 Whitelist IP - IA Factory

Liste des adresses IP à autoriser pour garantir une connectivité sécurisée avec les connecteurs IA Factory.

---

## 📑 Table des Matières

1. [Introduction](#introduction)
2. [Adresses IP à Whitelister](#adresses-ip-à-whitelister)
3. [Pourquoi Whitelister ?](#pourquoi-whitelister-)
4. [Configuration par Pare-feu](#configuration-par-pare-feu)
5. [Configuration par Service](#configuration-par-service)
6. [Vérification de la Configuration](#vérification-de-la-configuration)
7. [Dépannage](#dépannage)
8. [Sécurité et Mises à Jour](#sécurité-et-mises-à-jour)

---

## 🎯 Introduction

Pour assurer une **connectivité sécurisée et ininterrompue** avec les connecteurs IA Factory (MCP Servers, intégrations tierces, webhooks), il est essentiel d'autoriser certaines adresses IP dans votre pare-feu réseau.

### Qui doit configurer le whitelist ?

✅ **Entreprises avec pare-feu réseau** (firewall d'entreprise)
✅ **Équipes IT gérant des serveurs on-premise**
✅ **Utilisateurs Enterprise avec connecteurs MCP personnalisés**
✅ **Intégrations avec bases de données internes** (PostgreSQL, MySQL)
✅ **Webhooks vers systèmes internes** (n8n, Zapier self-hosted)

❌ **Utilisateurs individuels sans pare-feu** (configuration automatique)

---

## 🌐 Adresses IP à Whitelister

### Serveurs IA Factory - Infrastructure Principale

**Région : Europe (Paris, France) + Algérie**

```
# Serveurs API principaux
185.98.136.10
185.98.136.11
185.98.136.12

# Serveurs de traitement LLM
185.98.137.20
185.98.137.21
185.98.137.22

# Serveurs connecteurs MCP
185.98.138.30
185.98.138.31
185.98.138.32

# Serveurs webhooks et callbacks
185.98.139.40
185.98.139.41

# Serveurs algériens (Algérie Télécom)
41.107.64.50
41.107.64.51
41.107.64.52
```

---

### Plages IP par Service

| Service | Adresses IP | Port | Protocole |
|---------|-------------|------|-----------|
| **API IA Factory** | 185.98.136.10-12 | 443 | HTTPS |
| **LLM Processing** | 185.98.137.20-22 | 443 | HTTPS |
| **MCP Servers** | 185.98.138.30-32 | 443, 5432, 3306 | HTTPS, PostgreSQL, MySQL |
| **Webhooks** | 185.98.139.40-41 | 443, 80 | HTTPS, HTTP |
| **Algérie (Local)** | 41.107.64.50-52 | 443 | HTTPS |

---

### Format CIDR (Pour Pare-feu Avancés)

```bash
# Infrastructure principale
185.98.136.0/24    # API et services core
185.98.137.0/24    # LLM et traitement IA
185.98.138.0/24    # Connecteurs MCP
185.98.139.0/24    # Webhooks et callbacks

# Infrastructure algérienne
41.107.64.0/24     # Serveurs Algérie Télécom
```

---

## 🔍 Pourquoi Whitelister ?

### Cas d'Usage Nécessitant le Whitelist

#### 1️⃣ **Connecteurs MCP vers Bases de Données Internes**

```
Scénario :
Votre entreprise utilise PostgreSQL on-premise pour la gestion
des stocks, et vous voulez connecter IA Factory pour des analyses
intelligentes via chat.

❌ Sans whitelist :
Les serveurs MCP d'IA Factory ne peuvent pas accéder à votre
base de données (bloqués par le firewall d'entreprise).

✅ Avec whitelist :
Accès sécurisé depuis les IPs 185.98.138.30-32 uniquement,
garantissant que seul IA Factory peut interroger votre base.
```

**Configuration PostgreSQL :**

```bash
# /etc/postgresql/14/main/pg_hba.conf
# Autoriser connexions IA Factory uniquement

# IA Factory MCP Servers
host    all    iafactory_user    185.98.138.30/32    md5
host    all    iafactory_user    185.98.138.31/32    md5
host    all    iafactory_user    185.98.138.32/32    md5

# Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

---

#### 2️⃣ **Webhooks vers Systèmes Internes**

```
Scénario :
Votre workflow n8n self-hosted doit recevoir des événements
d'IA Factory (nouveau document uploadé, tâche terminée, etc.).

Configuration n8n :
1. Créer webhook : https://n8n.votreentreprise.dz/webhook/iafactory
2. Whitelister IPs : 185.98.139.40-41
3. Vérifier : Événement reçu et traité
```

**Exemple de workflow n8n :**

```json
{
  "nodes": [
    {
      "name": "IA Factory Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "path": "iafactory",
        "responseMode": "onReceived",
        "options": {
          "ipWhitelist": "185.98.139.40,185.98.139.41"
        }
      }
    },
    {
      "name": "Process Document",
      "type": "n8n-nodes-base.function",
      "position": [450, 300],
      "parameters": {
        "functionCode": "// Traiter document uploadé\nconst docId = items[0].json.document_id;\nreturn [{json: {status: 'processed', docId}}];"
      }
    }
  ]
}
```

---

#### 3️⃣ **Intégrations API Bidirectionnelles**

```
Scénario :
Votre ERP interne (Odoo self-hosted) doit synchroniser les
commandes clients avec IA Factory pour génération automatique
de factures et rapports.

Configuration Odoo :
1. Module : Whitelist IPs dans Odoo Security
2. IPs autorisées : 185.98.136.10-12 (API IA Factory)
3. Endpoint : /api/v1/erp/sync
```

---

## ⚙️ Configuration par Pare-feu

### 1️⃣ iptables (Linux)

```bash
#!/bin/bash
# Script de configuration iptables pour IA Factory

# Autoriser API IA Factory (HTTPS)
iptables -A INPUT -p tcp -s 185.98.136.10 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.136.11 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.136.12 --dport 443 -j ACCEPT

# Autoriser serveurs LLM
iptables -A INPUT -p tcp -s 185.98.137.20 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.137.21 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.137.22 --dport 443 -j ACCEPT

# Autoriser MCP Servers (PostgreSQL + MySQL)
iptables -A INPUT -p tcp -s 185.98.138.30 --dport 5432 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.138.31 --dport 5432 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.138.32 --dport 5432 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.138.30 --dport 3306 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.138.31 --dport 3306 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.138.32 --dport 3306 -j ACCEPT

# Autoriser Webhooks
iptables -A INPUT -p tcp -s 185.98.139.40 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.139.40 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.139.41 --dport 80 -j ACCEPT
iptables -A INPUT -p tcp -s 185.98.139.41 --dport 443 -j ACCEPT

# Serveurs algériens
iptables -A INPUT -p tcp -s 41.107.64.50 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 41.107.64.51 --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 41.107.64.52 --dport 443 -j ACCEPT

# Sauvegarder les règles
iptables-save > /etc/iptables/rules.v4

echo "✅ Whitelist IA Factory configuré avec succès"
```

---

### 2️⃣ UFW (Ubuntu Firewall)

```bash
#!/bin/bash
# Configuration UFW pour IA Factory

# API IA Factory
ufw allow from 185.98.136.10 to any port 443 proto tcp
ufw allow from 185.98.136.11 to any port 443 proto tcp
ufw allow from 185.98.136.12 to any port 443 proto tcp

# Serveurs LLM
ufw allow from 185.98.137.20 to any port 443 proto tcp
ufw allow from 185.98.137.21 to any port 443 proto tcp
ufw allow from 185.98.137.22 to any port 443 proto tcp

# MCP Servers (PostgreSQL)
ufw allow from 185.98.138.30 to any port 5432 proto tcp
ufw allow from 185.98.138.31 to any port 5432 proto tcp
ufw allow from 185.98.138.32 to any port 5432 proto tcp

# MCP Servers (MySQL)
ufw allow from 185.98.138.30 to any port 3306 proto tcp
ufw allow from 185.98.138.31 to any port 3306 proto tcp
ufw allow from 185.98.138.32 to any port 3306 proto tcp

# Webhooks
ufw allow from 185.98.139.40 to any port 80,443 proto tcp
ufw allow from 185.98.139.41 to any port 80,443 proto tcp

# Serveurs algériens
ufw allow from 41.107.64.50 to any port 443 proto tcp
ufw allow from 41.107.64.51 to any port 443 proto tcp
ufw allow from 41.107.64.52 to any port 443 proto tcp

# Recharger UFW
ufw reload

echo "✅ UFW configuré pour IA Factory"
```

---

### 3️⃣ Windows Firewall

**Via PowerShell (Administrateur) :**

```powershell
# Configuration Windows Firewall pour IA Factory

# API IA Factory
New-NetFirewallRule -DisplayName "IA Factory API 1" -Direction Inbound -RemoteAddress 185.98.136.10 -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory API 2" -Direction Inbound -RemoteAddress 185.98.136.11 -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory API 3" -Direction Inbound -RemoteAddress 185.98.136.12 -Protocol TCP -LocalPort 443 -Action Allow

# Serveurs LLM
New-NetFirewallRule -DisplayName "IA Factory LLM 1" -Direction Inbound -RemoteAddress 185.98.137.20 -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory LLM 2" -Direction Inbound -RemoteAddress 185.98.137.21 -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory LLM 3" -Direction Inbound -RemoteAddress 185.98.137.22 -Protocol TCP -LocalPort 443 -Action Allow

# MCP Servers PostgreSQL
New-NetFirewallRule -DisplayName "IA Factory MCP PG 1" -Direction Inbound -RemoteAddress 185.98.138.30 -Protocol TCP -LocalPort 5432 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory MCP PG 2" -Direction Inbound -RemoteAddress 185.98.138.31 -Protocol TCP -LocalPort 5432 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory MCP PG 3" -Direction Inbound -RemoteAddress 185.98.138.32 -Protocol TCP -LocalPort 5432 -Action Allow

# MCP Servers MySQL
New-NetFirewallRule -DisplayName "IA Factory MCP MySQL 1" -Direction Inbound -RemoteAddress 185.98.138.30 -Protocol TCP -LocalPort 3306 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory MCP MySQL 2" -Direction Inbound -RemoteAddress 185.98.138.31 -Protocol TCP -LocalPort 3306 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory MCP MySQL 3" -Direction Inbound -RemoteAddress 185.98.138.32 -Protocol TCP -LocalPort 3306 -Action Allow

# Webhooks
New-NetFirewallRule -DisplayName "IA Factory Webhook 1" -Direction Inbound -RemoteAddress 185.98.139.40 -Protocol TCP -LocalPort 80,443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory Webhook 2" -Direction Inbound -RemoteAddress 185.98.139.41 -Protocol TCP -LocalPort 80,443 -Action Allow

# Serveurs algériens
New-NetFirewallRule -DisplayName "IA Factory Algérie 1" -Direction Inbound -RemoteAddress 41.107.64.50 -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory Algérie 2" -Direction Inbound -RemoteAddress 41.107.64.51 -Protocol TCP -LocalPort 443 -Action Allow
New-NetFirewallRule -DisplayName "IA Factory Algérie 3" -Direction Inbound -RemoteAddress 41.107.64.52 -Protocol TCP -LocalPort 443 -Action Allow

Write-Host "✅ Windows Firewall configuré pour IA Factory" -ForegroundColor Green
```

---

### 4️⃣ pfSense / OPNsense

**Via Interface Web :**

```
Navigation :
Firewall → Rules → WAN → Add

Configuration pour chaque IP :
┌────────────────────────────────────────┐
│ Action : ☑ Pass                        │
│ Interface : WAN                        │
│ Address Family : IPv4                  │
│ Protocol : TCP                         │
│                                        │
│ Source :                               │
│   Type : Single host or alias          │
│   Address : 185.98.136.10              │
│                                        │
│ Destination :                          │
│   Type : This firewall (self)          │
│   Port range : HTTPS (443)             │
│                                        │
│ Description : IA Factory API Server 1  │
│                                        │
│ [Save] [Cancel]                        │
└────────────────────────────────────────┘

Répéter pour toutes les IPs listées.
```

---

### 5️⃣ AWS Security Groups

**Via AWS Console ou CLI :**

```bash
# Configuration Security Group pour IA Factory

# Créer Security Group
aws ec2 create-security-group \
  --group-name iafactory-whitelist \
  --description "Whitelist IA Factory IPs" \
  --vpc-id vpc-xxxxx

# Récupérer ID du Security Group
SG_ID=$(aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=iafactory-whitelist" \
  --query "SecurityGroups[0].GroupId" --output text)

# Autoriser API IA Factory (HTTPS)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges='[{CidrIp=185.98.136.10/32,Description="IA Factory API 1"}]'

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges='[{CidrIp=185.98.136.11/32,Description="IA Factory API 2"}]'

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --ip-permissions IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges='[{CidrIp=185.98.136.12/32,Description="IA Factory API 3"}]'

# Autoriser MCP PostgreSQL
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --ip-permissions IpProtocol=tcp,FromPort=5432,ToPort=5432,IpRanges='[{CidrIp=185.98.138.30/32,Description="IA Factory MCP 1"}]'

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --ip-permissions IpProtocol=tcp,FromPort=5432,ToPort=5432,IpRanges='[{CidrIp=185.98.138.31/32,Description="IA Factory MCP 2"}]'

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --ip-permissions IpProtocol=tcp,FromPort=5432,ToPort=5432,IpRanges='[{CidrIp=185.98.138.32/32,Description="IA Factory MCP 3"}]'

# Attacher à instance EC2
aws ec2 modify-instance-attribute \
  --instance-id i-xxxxx \
  --groups $SG_ID

echo "✅ Security Group IA Factory configuré"
```

---

### 6️⃣ Google Cloud Firewall

**Via gcloud CLI :**

```bash
# Configuration Google Cloud Firewall pour IA Factory

# Autoriser API IA Factory
gcloud compute firewall-rules create iafactory-api \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:443 \
  --source-ranges=185.98.136.10/32,185.98.136.11/32,185.98.136.12/32 \
  --description="IA Factory API Servers"

# Autoriser serveurs LLM
gcloud compute firewall-rules create iafactory-llm \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:443 \
  --source-ranges=185.98.137.20/32,185.98.137.21/32,185.98.137.22/32 \
  --description="IA Factory LLM Servers"

# Autoriser MCP PostgreSQL
gcloud compute firewall-rules create iafactory-mcp-postgres \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:5432 \
  --source-ranges=185.98.138.30/32,185.98.138.31/32,185.98.138.32/32 \
  --description="IA Factory MCP PostgreSQL"

# Autoriser Webhooks
gcloud compute firewall-rules create iafactory-webhooks \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:80,tcp:443 \
  --source-ranges=185.98.139.40/32,185.98.139.41/32 \
  --description="IA Factory Webhooks"

# Serveurs algériens
gcloud compute firewall-rules create iafactory-algeria \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:443 \
  --source-ranges=41.107.64.50/32,41.107.64.51/32,41.107.64.52/32 \
  --description="IA Factory Algeria Servers"

echo "✅ Google Cloud Firewall configuré"
```

---

## 🔧 Configuration par Service

### PostgreSQL

**Fichier : `/etc/postgresql/14/main/pg_hba.conf`**

```bash
# IA Factory MCP Servers - Whitelist IP
# TYPE  DATABASE  USER              ADDRESS            METHOD

# Production database
host    prod_db   iafactory_user    185.98.138.30/32   scram-sha-256
host    prod_db   iafactory_user    185.98.138.31/32   scram-sha-256
host    prod_db   iafactory_user    185.98.138.32/32   scram-sha-256

# Analytics database (read-only)
host    analytics iafactory_ro      185.98.138.30/32   scram-sha-256
host    analytics iafactory_ro      185.98.138.31/32   scram-sha-256
host    analytics iafactory_ro      185.98.138.32/32   scram-sha-256

# Redémarrer PostgreSQL
# sudo systemctl restart postgresql
```

**Créer utilisateur PostgreSQL pour IA Factory :**

```sql
-- Créer utilisateur avec permissions limitées
CREATE USER iafactory_user WITH PASSWORD 'votre_mot_de_passe_securise';

-- Accorder permissions lecture/écriture
GRANT CONNECT ON DATABASE prod_db TO iafactory_user;
GRANT USAGE ON SCHEMA public TO iafactory_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO iafactory_user;

-- Utilisateur lecture seule pour analytics
CREATE USER iafactory_ro WITH PASSWORD 'mot_de_passe_ro';
GRANT CONNECT ON DATABASE analytics TO iafactory_ro;
GRANT USAGE ON SCHEMA public TO iafactory_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO iafactory_ro;
```

---

### MySQL

**Fichier : `/etc/mysql/mysql.conf.d/mysqld.cnf`**

```ini
[mysqld]
# Bind à toutes les interfaces (ou IP spécifique)
bind-address = 0.0.0.0

# OU bind à IP spécifique du serveur
# bind-address = 192.168.1.100

# Redémarrer MySQL
# sudo systemctl restart mysql
```

**Créer utilisateur MySQL pour IA Factory :**

```sql
-- Créer utilisateur avec accès limité aux IPs IA Factory
CREATE USER 'iafactory_user'@'185.98.138.30' IDENTIFIED BY 'mot_de_passe_securise';
CREATE USER 'iafactory_user'@'185.98.138.31' IDENTIFIED BY 'mot_de_passe_securise';
CREATE USER 'iafactory_user'@'185.98.138.32' IDENTIFIED BY 'mot_de_passe_securise';

-- Accorder permissions
GRANT SELECT, INSERT, UPDATE ON prod_db.* TO 'iafactory_user'@'185.98.138.30';
GRANT SELECT, INSERT, UPDATE ON prod_db.* TO 'iafactory_user'@'185.98.138.31';
GRANT SELECT, INSERT, UPDATE ON prod_db.* TO 'iafactory_user'@'185.98.138.32';

-- Appliquer changements
FLUSH PRIVILEGES;
```

---

### MongoDB

**Fichier : `/etc/mongod.conf`**

```yaml
# Configuration réseau
net:
  port: 27017
  bindIp: 0.0.0.0  # Accepter toutes connexions (sécurisé par firewall)

# Activer authentification
security:
  authorization: enabled

# Whitelist IP dans le firewall (iptables/ufw)
```

**Créer utilisateur MongoDB :**

```javascript
// Connexion à MongoDB
use admin

// Créer utilisateur pour IA Factory
db.createUser({
  user: "iafactory_user",
  pwd: "mot_de_passe_securise",
  roles: [
    { role: "readWrite", db: "prod_db" },
    { role: "read", db: "analytics" }
  ]
})

// Tester connexion
db.auth("iafactory_user", "mot_de_passe_securise")
```

---

### Redis

**Fichier : `/etc/redis/redis.conf`**

```bash
# Bind à IP spécifique
bind 0.0.0.0

# Activer authentification
requirepass votre_mot_de_passe_redis_securise

# Désactiver commandes dangereuses
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG ""

# Redémarrer Redis
# sudo systemctl restart redis
```

---

### Nginx (Reverse Proxy)

**Fichier : `/etc/nginx/sites-available/iafactory-webhook`**

```nginx
# Webhook endpoint pour IA Factory
server {
    listen 443 ssl http2;
    server_name webhook.votreentreprise.dz;

    ssl_certificate /etc/letsencrypt/live/webhook.votreentreprise.dz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/webhook.votreentreprise.dz/privkey.pem;

    # Whitelist IPs IA Factory uniquement
    allow 185.98.139.40;
    allow 185.98.139.41;
    deny all;

    location /iafactory {
        proxy_pass http://localhost:5678/webhook/iafactory;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Logs pour debugging
        access_log /var/log/nginx/iafactory-webhook-access.log;
        error_log /var/log/nginx/iafactory-webhook-error.log;
    }
}
```

---

## ✅ Vérification de la Configuration

### Test de Connectivité

**1. Depuis IA Factory (On vous fournit un outil de test) :**

```
Hub IA → ⚙️ Paramètres → 🔌 Connecteurs → 🧪 Test Connexion
```

**Interface de test :**

```
┌─────────────────────────────────────────────────────┐
│  🧪 Test de Connexion - PostgreSQL                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Host : db.votreentreprise.dz                       │
│  Port : 5432                                        │
│  Database : prod_db                                 │
│  User : iafactory_user                              │
│  Password : ••••••••••••••                          │
│                                                     │
│  [🧪 Tester la Connexion]                           │
│                                                     │
│  ⏳ Test en cours depuis 185.98.138.30...           │
│                                                     │
│  ✅ Connexion réussie !                             │
│  ⏱️ Latence : 45 ms                                 │
│  📊 Tables trouvées : 24                            │
│  💾 Taille DB : 2.3 GB                              │
│                                                     │
│  📝 Log :                                           │
│  [2024-01-15 10:30:45] Connexion établie           │
│  [2024-01-15 10:30:45] Auth réussie (scram-sha-256)│
│  [2024-01-15 10:30:45] SELECT version() OK         │
│  [2024-01-15 10:30:46] Liste tables OK             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

**2. Test manuel depuis votre serveur :**

```bash
# Test connectivité API IA Factory
curl -v https://api.iafactory.dz/health

# Résultat attendu :
# < HTTP/2 200
# < content-type: application/json
# {"status":"ok","version":"1.0.0","region":"eu-west-1"}

# Test depuis serveur database
# Vérifier logs PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Vous devriez voir :
# [2024-01-15 10:30:45 UTC] LOG: connection authorized: user=iafactory_user database=prod_db application_name=iafactory-mcp
```

---

### Monitoring des Connexions

**Script de monitoring en temps réel :**

```bash
#!/bin/bash
# monitor-iafactory-connections.sh

echo "🔍 Monitoring Connexions IA Factory"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

while true; do
    clear
    echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    echo "🔗 Connexions PostgreSQL actives :"
    sudo -u postgres psql -c "
        SELECT
            client_addr,
            usename,
            datname,
            state,
            query_start
        FROM pg_stat_activity
        WHERE client_addr IN (
            '185.98.138.30',
            '185.98.138.31',
            '185.98.138.32'
        )
        ORDER BY query_start DESC;
    "

    echo ""
    echo "🌐 Connexions réseau actives (port 5432) :"
    netstat -an | grep ':5432' | grep ESTABLISHED | grep -E '185\.98\.138\.(30|31|32)'

    echo ""
    echo "📊 Statistiques :"
    echo "  Connexions totales : $(netstat -an | grep ':5432' | grep ESTABLISHED | wc -l)"
    echo "  Depuis IA Factory : $(netstat -an | grep ':5432' | grep ESTABLISHED | grep -E '185\.98\.138\.(30|31|32)' | wc -l)"

    sleep 5
done
```

---

## 🛠️ Dépannage

### ❌ "Connection timeout"

```
Symptôme :
Timeout lors de la tentative de connexion depuis IA Factory

Causes possibles :
1. Pare-feu bloque les IPs IA Factory
2. Service base de données non démarré
3. Port non ouvert dans le pare-feu

Solutions :
```

```bash
# 1. Vérifier que le service est actif
sudo systemctl status postgresql
# OU
sudo systemctl status mysql

# 2. Vérifier que le port est ouvert
sudo netstat -tulpn | grep 5432  # PostgreSQL
sudo netstat -tulpn | grep 3306  # MySQL

# 3. Vérifier règles firewall
sudo iptables -L -n -v | grep 185.98.138

# 4. Tester connectivité locale
psql -h localhost -U iafactory_user -d prod_db

# 5. Vérifier logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

---

### ❌ "Connection refused"

```
Symptôme :
Connexion refusée immédiatement (pas de timeout)

Causes possibles :
1. Service non démarré sur le bon port
2. bind-address incorrect (127.0.0.1 au lieu de 0.0.0.0)
3. Pare-feu système (iptables) bloque

Solutions :
```

```bash
# PostgreSQL : Vérifier bind address
sudo grep "listen_addresses" /etc/postgresql/14/main/postgresql.conf
# Doit être : listen_addresses = '*'

# MySQL : Vérifier bind address
sudo grep "bind-address" /etc/mysql/mysql.conf.d/mysqld.cnf
# Doit être : bind-address = 0.0.0.0

# Redémarrer après modification
sudo systemctl restart postgresql
sudo systemctl restart mysql
```

---

### ❌ "Authentication failed"

```
Symptôme :
Connexion établie mais authentification échoue

Causes possibles :
1. Mot de passe incorrect
2. Utilisateur pas créé pour les bonnes IPs
3. Méthode d'authentification incompatible

Solutions :
```

```sql
-- PostgreSQL : Vérifier utilisateurs
SELECT * FROM pg_user WHERE usename = 'iafactory_user';

-- Recréer utilisateur si nécessaire
DROP USER IF EXISTS iafactory_user;
CREATE USER iafactory_user WITH PASSWORD 'nouveau_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE prod_db TO iafactory_user;

-- MySQL : Vérifier hosts autorisés
SELECT user, host FROM mysql.user WHERE user = 'iafactory_user';

-- Si host = 'localhost', supprimer et recréer
DROP USER 'iafactory_user'@'localhost';
CREATE USER 'iafactory_user'@'185.98.138.30' IDENTIFIED BY 'mot_de_passe';
```

---

### ❌ "SSL/TLS handshake failed"

```
Symptôme :
Erreur de négociation SSL/TLS

Causes possibles :
1. Certificat SSL expiré/invalide
2. Version TLS incompatible
3. Configuration SSL manquante

Solutions :
```

```bash
# PostgreSQL : Activer SSL
sudo nano /etc/postgresql/14/main/postgresql.conf
# Ajouter :
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'
ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'

# Modifier pg_hba.conf pour exiger SSL
sudo nano /etc/postgresql/14/main/pg_hba.conf
# Remplacer 'host' par 'hostssl'
hostssl  prod_db  iafactory_user  185.98.138.30/32  scram-sha-256

# Redémarrer
sudo systemctl restart postgresql
```

---

### 🧪 Script de Diagnostic Complet

```bash
#!/bin/bash
# diagnostic-iafactory.sh

echo "🔍 Diagnostic IA Factory Whitelist"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Vérifier services
echo ""
echo "1️⃣ État des Services"
systemctl is-active postgresql && echo "  ✅ PostgreSQL actif" || echo "  ❌ PostgreSQL inactif"
systemctl is-active mysql && echo "  ✅ MySQL actif" || echo "  ❌ MySQL inactif"
systemctl is-active redis && echo "  ✅ Redis actif" || echo "  ❌ Redis inactif"

# 2. Vérifier ports ouverts
echo ""
echo "2️⃣ Ports Ouverts"
netstat -tulpn | grep -E ':5432|:3306|:6379|:443|:80' | while read line; do
    echo "  ℹ️  $line"
done

# 3. Vérifier règles firewall
echo ""
echo "3️⃣ Règles Firewall pour IA Factory"
iptables -L -n -v | grep -E '185\.98\.(136|137|138|139)|41\.107\.64' | while read line; do
    echo "  ✅ $line"
done

# 4. Tester connectivité vers API IA Factory
echo ""
echo "4️⃣ Test Connectivité API IA Factory"
if curl -s --max-time 5 https://api.iafactory.dz/health > /dev/null; then
    echo "  ✅ API IA Factory accessible"
else
    echo "  ❌ API IA Factory inaccessible"
fi

# 5. Vérifier logs récents
echo ""
echo "5️⃣ Logs Récents (5 dernières lignes)"
echo "  📄 PostgreSQL :"
sudo tail -n 5 /var/log/postgresql/postgresql-14-main.log | sed 's/^/     /'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Diagnostic terminé"
```

---

## 🔄 Sécurité et Mises à Jour

### Notifications de Changement d'IP

```
IA Factory vous notifie 30 jours à l'avance en cas de changement d'IP :

📧 Email : security@iafactory.dz
📬 Notification dans Hub IA
📱 SMS (comptes Enterprise)
📣 Annonce sur status.iafactory.dz
```

**Exemple de notification :**

```
┌─────────────────────────────────────────────────────┐
│  ⚠️ MISE À JOUR WHITELIST IP - 30 JOURS             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Bonjour,                                           │
│                                                     │
│  Dans le cadre de l'expansion de notre             │
│  infrastructure, nous ajouterons de nouvelles       │
│  adresses IP le 15 février 2025.                    │
│                                                     │
│  📅 Date de changement : 15/02/2025                 │
│  🆕 Nouvelles IPs à whitelister :                   │
│     • 185.98.140.10 (API serveur 4)                 │
│     • 185.98.140.11 (API serveur 5)                 │
│                                                     │
│  ⚠️ Les anciennes IPs resteront actives jusqu'au    │
│     15/03/2025 pour transition en douceur.          │
│                                                     │
│  📝 Action requise :                                │
│  Ajoutez ces IPs à votre whitelist avant le         │
│  15 février 2025.                                   │
│                                                     │
│  📧 Questions : security@iafactory.dz               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### Page de Statut en Temps Réel

**URL : https://status.iafactory.dz**

```
┌─────────────────────────────────────────────────────┐
│  📊 Statut IA Factory - Tous Systèmes Opérationnels │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🟢 API Principale (185.98.136.10-12)               │
│     Uptime : 99.99% | Latence : 12 ms               │
│                                                     │
│  🟢 Serveurs LLM (185.98.137.20-22)                 │
│     Uptime : 99.98% | Latence : 45 ms               │
│                                                     │
│  🟢 MCP Servers (185.98.138.30-32)                  │
│     Uptime : 99.97% | Latence : 8 ms                │
│                                                     │
│  🟢 Webhooks (185.98.139.40-41)                     │
│     Uptime : 99.99% | Latence : 15 ms               │
│                                                     │
│  🟢 Serveurs Algérie (41.107.64.50-52)              │
│     Uptime : 99.95% | Latence : 25 ms               │
│                                                     │
│  📅 Dernière mise à jour : Il y a 2 minutes         │
│                                                     │
│  📜 Historique : Aucun incident dans les 90 jours   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

### Bonnes Pratiques de Sécurité

```
✅ Principe du moindre privilège
   • N'autorisez que les IPs strictement nécessaires
   • Créez des utilisateurs DB avec permissions minimales

✅ Rotation des credentials
   • Changez mots de passe tous les 90 jours
   • Utilisez des mots de passe forts (20+ caractères)

✅ Monitoring et logs
   • Activez logs d'audit pour toutes connexions
   • Surveillez tentatives d'accès échouées
   • Alertes en cas d'activité suspecte

✅ Chiffrement obligatoire
   • Utilisez SSL/TLS pour toutes connexions DB
   • Vérifiez certificats côté client

✅ Sauvegarde du whitelist
   • Documentez toutes les règles firewall
   • Sauvegardez configurations (version control)
   • Testez procédure de restauration

✅ Mise à jour régulière
   • Suivez status.iafactory.dz pour annonces
   • Inscrivez-vous à newsletter sécurité
   • Auditez whitelist trimestriellement
```

---

## 📞 Support

### Besoin d'Aide ?

```
📧 Email Sécurité : security@iafactory.dz
💬 Chat Support : Hub IA → 💬 Support (24/7)
📱 WhatsApp Enterprise : +213 560 XX XX XX
📞 Hotline : +213 21 XX XX XX (Lun-Ven 9h-18h)
```

### Documentation Complémentaire

- 🔌 [Connecteurs MCP](CONNECTEURS_IAFACTORY.md)
- 🔐 [Sécurité et Confidentialité](SECURITE_DONNEES.md)
- 📊 [Guide PostgreSQL MCP](CONNECTEURS_IAFACTORY.md#postgresql)
- ⚙️ [Configuration API](INDEX_IAFACTORY.md)

---

**🇩🇿 IA Factory - Infrastructure Sécurisée Made in Algeria**

*Documentation mise à jour : Janvier 2025*

---

## 📋 Checklist Rapide

```
☐ Identifier services nécessitant whitelist
☐ Récupérer liste IPs IA Factory (ce document)
☐ Configurer pare-feu (iptables/UFW/Windows/Cloud)
☐ Configurer services (PostgreSQL/MySQL/MongoDB/Redis)
☐ Tester connectivité (outil IA Factory)
☐ Vérifier logs (connexions réussies)
☐ Activer monitoring
☐ Documenter configuration
☐ S'inscrire notifications (status.iafactory.dz)
☐ Planifier revue trimestrielle
```

---

**Note importante :** Les adresses IP listées dans ce document sont fictives mais réalistes pour l'infrastructure IA Factory. En production, IA Factory fournira les IPs réelles via le portail Enterprise et par email sécurisé.
