"""
IA Factory Automation - Multi-tenant Infrastructure
Architecture Proxmox + LXC pour héberger 20+ clients par serveur
Optimisé pour TOPTON i9-14900 (24 cores, 64GB DDR5)
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import asyncio
import json
import os

router = APIRouter(prefix="/infra", tags=["Multi-tenant Infrastructure"])


class TenantTier(str, Enum):
    STARTER = "Starter"      # 500 CHF/mois
    PROFESSIONAL = "Pro"     # 1200 CHF/mois
    ENTERPRISE = "Enterprise"  # 3000 CHF/mois


class TenantStatus(str, Enum):
    PENDING = "pending"
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class Region(str, Enum):
    CH = "ch-geneva"      # Infomaniak Suisse
    DZ = "dz-alger"       # ICOSNET Algérie
    DEV = "dev-hetzner"   # Hetzner Allemagne


class ServiceType(str, Enum):
    RAG = "rag"
    CHATBOT = "chatbot"
    VOICE_ASSISTANT = "voice"
    TEACHING = "teaching"
    LEGAL = "legal"
    CUSTOM = "custom"


# ===== RESOURCE ALLOCATION =====

TIER_RESOURCES = {
    TenantTier.STARTER: {
        "cpu_cores": 2,
        "ram_gb": 4,
        "disk_gb": 50,
        "gpu_share": 0,
        "concurrent_users": 10,
        "api_calls_month": 10000,
        "price_chf": 500,
        "price_dzd": 50000
    },
    TenantTier.PROFESSIONAL: {
        "cpu_cores": 4,
        "ram_gb": 8,
        "disk_gb": 100,
        "gpu_share": 0.25,
        "concurrent_users": 50,
        "api_calls_month": 50000,
        "price_chf": 1200,
        "price_dzd": 100000
    },
    TenantTier.ENTERPRISE: {
        "cpu_cores": 8,
        "ram_gb": 16,
        "disk_gb": 250,
        "gpu_share": 0.5,
        "concurrent_users": 200,
        "api_calls_month": 200000,
        "price_chf": 3000,
        "price_dzd": 250000
    }
}

# Configuration serveur TOPTON
SERVER_SPECS = {
    "model": "TOPTON i9-14900",
    "total_cores": 24,
    "total_ram_gb": 64,
    "total_disk_gb": 2000,  # 2TB NVMe
    "max_tenants_per_tier": {
        TenantTier.STARTER: 20,
        TenantTier.PROFESSIONAL: 10,
        TenantTier.ENTERPRISE: 4
    }
}


# ===== MODELS =====

class TenantRequest(BaseModel):
    """Requête de création de tenant"""
    company_name: str
    contact_email: str
    tier: TenantTier
    region: Region
    services: List[ServiceType]
    custom_domain: Optional[str] = None
    billing_currency: str = "CHF"


class Tenant(BaseModel):
    """Tenant (client hébergé)"""
    id: str
    company_name: str
    contact_email: str
    tier: TenantTier
    region: Region
    status: TenantStatus
    services: List[ServiceType]
    resources: Dict[str, Any]
    container_id: Optional[str] = None
    custom_domain: Optional[str] = None
    created_at: datetime
    last_active: Optional[datetime] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)


class ContainerConfig(BaseModel):
    """Configuration conteneur LXC"""
    hostname: str
    cpu_cores: int
    ram_mb: int
    disk_gb: int
    network: str
    template: str
    startup_script: str


class ServerNode(BaseModel):
    """Noeud serveur physique"""
    id: str
    name: str
    region: Region
    specs: Dict[str, Any]
    total_capacity: Dict[str, int]
    used_capacity: Dict[str, int]
    tenants: List[str]
    status: str = "active"


class InfrastructureMetrics(BaseModel):
    """Métriques d'infrastructure"""
    total_tenants: int
    tenants_by_tier: Dict[str, int]
    tenants_by_region: Dict[str, int]
    resource_utilization: Dict[str, float]
    revenue_monthly: Dict[str, float]
    projected_capacity: int


# ===== MULTI-TENANT MANAGER =====

class MultiTenantManager:
    """
    Gestionnaire multi-tenant
    Provisionne et gère les environnements clients isolés
    """
    
    def __init__(self):
        self.tenants: Dict[str, Tenant] = {}
        self.servers: Dict[str, ServerNode] = {}
        self._initialize_servers()
    
    def _initialize_servers(self):
        """Initialise les serveurs disponibles"""
        
        # Serveur CH (Infomaniak)
        self.servers["ch-01"] = ServerNode(
            id="ch-01",
            name="ia-factory-ch-01",
            region=Region.CH,
            specs=SERVER_SPECS,
            total_capacity={
                "cpu_cores": 24,
                "ram_gb": 64,
                "disk_gb": 2000
            },
            used_capacity={
                "cpu_cores": 0,
                "ram_gb": 0,
                "disk_gb": 0
            },
            tenants=[]
        )
        
        # Serveur DZ (ICOSNET)
        self.servers["dz-01"] = ServerNode(
            id="dz-01",
            name="ia-factory-dz-01",
            region=Region.DZ,
            specs=SERVER_SPECS,
            total_capacity={
                "cpu_cores": 24,
                "ram_gb": 64,
                "disk_gb": 2000
            },
            used_capacity={
                "cpu_cores": 0,
                "ram_gb": 0,
                "disk_gb": 0
            },
            tenants=[]
        )
        
        # Serveur Dev (Hetzner)
        self.servers["dev-01"] = ServerNode(
            id="dev-01",
            name="ia-factory-dev-01",
            region=Region.DEV,
            specs={
                "model": "Hetzner VPS",
                "total_cores": 8,
                "total_ram_gb": 16,
                "total_disk_gb": 200
            },
            total_capacity={
                "cpu_cores": 8,
                "ram_gb": 16,
                "disk_gb": 200
            },
            used_capacity={
                "cpu_cores": 0,
                "ram_gb": 0,
                "disk_gb": 0
            },
            tenants=[]
        )
    
    def _select_server(self, region: Region, tier: TenantTier) -> Optional[str]:
        """Sélectionne le serveur optimal pour le tenant"""
        
        resources = TIER_RESOURCES[tier]
        
        for server_id, server in self.servers.items():
            if server.region != region:
                continue
            
            if server.status != "active":
                continue
            
            # Vérifier la capacité
            available_cpu = server.total_capacity["cpu_cores"] - server.used_capacity["cpu_cores"]
            available_ram = server.total_capacity["ram_gb"] - server.used_capacity["ram_gb"]
            available_disk = server.total_capacity["disk_gb"] - server.used_capacity["disk_gb"]
            
            if (available_cpu >= resources["cpu_cores"] and
                available_ram >= resources["ram_gb"] and
                available_disk >= resources["disk_gb"]):
                return server_id
        
        return None
    
    async def create_tenant(self, request: TenantRequest) -> Tenant:
        """Crée un nouveau tenant"""
        
        # Sélectionner le serveur
        server_id = self._select_server(request.region, request.tier)
        
        if not server_id:
            raise ValueError(f"No available capacity in region {request.region.value}")
        
        # Générer ID unique
        tenant_id = f"tenant_{datetime.now().strftime('%Y%m%d%H%M%S')}_{request.company_name[:8].replace(' ', '_').lower()}"
        
        # Ressources allouées
        resources = TIER_RESOURCES[request.tier]
        
        # Créer le tenant
        tenant = Tenant(
            id=tenant_id,
            company_name=request.company_name,
            contact_email=request.contact_email,
            tier=request.tier,
            region=request.region,
            status=TenantStatus.PROVISIONING,
            services=request.services,
            resources=resources,
            custom_domain=request.custom_domain,
            created_at=datetime.now(),
            metrics={
                "api_calls": 0,
                "storage_used_gb": 0,
                "active_users": 0
            }
        )
        
        # Sauvegarder
        self.tenants[tenant_id] = tenant
        
        # Mettre à jour la capacité du serveur
        server = self.servers[server_id]
        server.used_capacity["cpu_cores"] += resources["cpu_cores"]
        server.used_capacity["ram_gb"] += resources["ram_gb"]
        server.used_capacity["disk_gb"] += resources["disk_gb"]
        server.tenants.append(tenant_id)
        
        # Provisionner le conteneur (async)
        container_config = await self._generate_container_config(tenant)
        tenant.container_id = container_config.hostname
        
        # Marquer comme actif
        tenant.status = TenantStatus.ACTIVE
        
        return tenant
    
    async def _generate_container_config(self, tenant: Tenant) -> ContainerConfig:
        """Génère la configuration du conteneur LXC"""
        
        resources = tenant.resources
        
        # Template selon les services
        if ServiceType.TEACHING in tenant.services:
            template = "debian-12-teaching"
        elif ServiceType.VOICE_ASSISTANT in tenant.services:
            template = "debian-12-voice"
        else:
            template = "debian-12-rag"
        
        # Script de démarrage
        startup_script = self._generate_startup_script(tenant)
        
        return ContainerConfig(
            hostname=f"lxc-{tenant.id}",
            cpu_cores=resources["cpu_cores"],
            ram_mb=resources["ram_gb"] * 1024,
            disk_gb=resources["disk_gb"],
            network="vmbr0",
            template=template,
            startup_script=startup_script
        )
    
    def _generate_startup_script(self, tenant: Tenant) -> str:
        """Génère le script de démarrage du conteneur"""
        
        services_setup = []
        
        for service in tenant.services:
            if service == ServiceType.RAG:
                services_setup.append("""
# Setup RAG service
docker-compose -f /opt/ia-factory/rag/docker-compose.yml up -d
""")
            elif service == ServiceType.CHATBOT:
                services_setup.append("""
# Setup Chatbot service
docker-compose -f /opt/ia-factory/chatbot/docker-compose.yml up -d
""")
            elif service == ServiceType.TEACHING:
                services_setup.append("""
# Setup Teaching Assistant
docker-compose -f /opt/ia-factory/teaching/docker-compose.yml up -d
""")
        
        return f"""#!/bin/bash
# Auto-generated startup script for {tenant.company_name}
# Tenant ID: {tenant.id}

set -e

# Update system
apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone IA Factory base
git clone https://github.com/iafactory/tenant-base.git /opt/ia-factory

# Configure environment
cat > /opt/ia-factory/.env <<EOF
TENANT_ID={tenant.id}
TENANT_TIER={tenant.tier.value}
API_KEY=$(openssl rand -hex 32)
EOF

# Setup services
{"".join(services_setup)}

# Setup Nginx reverse proxy
cat > /etc/nginx/sites-available/{tenant.id} <<EOF
server {{
    listen 80;
    server_name {tenant.custom_domain or f'{tenant.id}.iafactory.ch'};
    
    location / {{
        proxy_pass http://localhost:8000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
    }}
}}
EOF

ln -s /etc/nginx/sites-available/{tenant.id} /etc/nginx/sites-enabled/
systemctl reload nginx

# Setup SSL with Let's Encrypt
certbot --nginx -d {tenant.custom_domain or f'{tenant.id}.iafactory.ch'} --non-interactive --agree-tos -m {tenant.contact_email}

echo "Tenant {tenant.id} setup complete!"
"""
    
    async def suspend_tenant(self, tenant_id: str) -> bool:
        """Suspend un tenant"""
        
        if tenant_id not in self.tenants:
            raise ValueError("Tenant not found")
        
        tenant = self.tenants[tenant_id]
        tenant.status = TenantStatus.SUSPENDED
        
        return True
    
    async def terminate_tenant(self, tenant_id: str) -> bool:
        """Termine un tenant et libère les ressources"""
        
        if tenant_id not in self.tenants:
            raise ValueError("Tenant not found")
        
        tenant = self.tenants[tenant_id]
        
        # Libérer les ressources du serveur
        for server_id, server in self.servers.items():
            if tenant_id in server.tenants:
                resources = tenant.resources
                server.used_capacity["cpu_cores"] -= resources["cpu_cores"]
                server.used_capacity["ram_gb"] -= resources["ram_gb"]
                server.used_capacity["disk_gb"] -= resources["disk_gb"]
                server.tenants.remove(tenant_id)
                break
        
        tenant.status = TenantStatus.TERMINATED
        
        return True
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Récupère un tenant par ID"""
        return self.tenants.get(tenant_id)
    
    def list_tenants(
        self,
        region: Optional[Region] = None,
        tier: Optional[TenantTier] = None,
        status: Optional[TenantStatus] = None
    ) -> List[Tenant]:
        """Liste les tenants avec filtres"""
        
        tenants = list(self.tenants.values())
        
        if region:
            tenants = [t for t in tenants if t.region == region]
        if tier:
            tenants = [t for t in tenants if t.tier == tier]
        if status:
            tenants = [t for t in tenants if t.status == status]
        
        return tenants
    
    def get_infrastructure_metrics(self) -> InfrastructureMetrics:
        """Calcule les métriques d'infrastructure"""
        
        active_tenants = [t for t in self.tenants.values() if t.status == TenantStatus.ACTIVE]
        
        # Par tier
        tenants_by_tier = {}
        for tier in TenantTier:
            tenants_by_tier[tier.value] = len([t for t in active_tenants if t.tier == tier])
        
        # Par région
        tenants_by_region = {}
        for region in Region:
            tenants_by_region[region.value] = len([t for t in active_tenants if t.region == region])
        
        # Utilisation ressources
        total_cpu = sum(s.total_capacity["cpu_cores"] for s in self.servers.values())
        used_cpu = sum(s.used_capacity["cpu_cores"] for s in self.servers.values())
        
        total_ram = sum(s.total_capacity["ram_gb"] for s in self.servers.values())
        used_ram = sum(s.used_capacity["ram_gb"] for s in self.servers.values())
        
        # Revenus mensuels
        revenue_chf = sum(
            TIER_RESOURCES[t.tier]["price_chf"] 
            for t in active_tenants 
            if t.region == Region.CH
        )
        revenue_dzd = sum(
            TIER_RESOURCES[t.tier]["price_dzd"] 
            for t in active_tenants 
            if t.region == Region.DZ
        )
        
        # Capacité restante
        remaining_starter = sum(
            (s.total_capacity["cpu_cores"] - s.used_capacity["cpu_cores"]) // TIER_RESOURCES[TenantTier.STARTER]["cpu_cores"]
            for s in self.servers.values()
        )
        
        return InfrastructureMetrics(
            total_tenants=len(active_tenants),
            tenants_by_tier=tenants_by_tier,
            tenants_by_region=tenants_by_region,
            resource_utilization={
                "cpu_percent": round(used_cpu / total_cpu * 100, 1) if total_cpu > 0 else 0,
                "ram_percent": round(used_ram / total_ram * 100, 1) if total_ram > 0 else 0
            },
            revenue_monthly={
                "CHF": revenue_chf,
                "DZD": revenue_dzd
            },
            projected_capacity=remaining_starter
        )
    
    def generate_proxmox_config(self) -> str:
        """Génère la configuration Proxmox pour tous les serveurs"""
        
        config = """
# Proxmox VE Configuration for IA Factory
# Multi-tenant Infrastructure

## Cluster Configuration
datacenter: ia-factory
ha-enabled: true

## Storage Configuration
storage: local-lvm
shared-storage: ceph

## Network Configuration
# Main bridge for tenant traffic
auto vmbr0
iface vmbr0 inet static
    address 10.0.0.1/24
    bridge-ports eth0
    bridge-stp off
    bridge-fd 0

# Management network
auto vmbr1
iface vmbr1 inet static
    address 192.168.1.1/24
    bridge-ports eth1
    bridge-stp off
    bridge-fd 0

## LXC Template Defaults
lxc.default.memory: 4096
lxc.default.cores: 2
lxc.default.disk: 50G
lxc.default.unprivileged: 1
lxc.default.features: nesting=1

## Resource Limits by Tier
"""
        
        for tier, resources in TIER_RESOURCES.items():
            config += f"""
# Tier: {tier.value}
# CPU: {resources['cpu_cores']} cores
# RAM: {resources['ram_gb']} GB
# Disk: {resources['disk_gb']} GB
# Max concurrent users: {resources['concurrent_users']}
"""
        
        return config
    
    def generate_terraform_config(self) -> str:
        """Génère la configuration Terraform pour l'infrastructure"""
        
        return """
# Terraform Configuration for IA Factory Multi-tenant
# Provider: Proxmox VE

terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "2.9.14"
    }
  }
}

variable "proxmox_url" {
  type = string
}

variable "proxmox_user" {
  type = string
}

variable "proxmox_password" {
  type      = string
  sensitive = true
}

provider "proxmox" {
  pm_api_url      = var.proxmox_url
  pm_user         = var.proxmox_user
  pm_password     = var.proxmox_password
  pm_tls_insecure = false
}

# LXC Container Template
resource "proxmox_lxc" "tenant_template" {
  target_node  = "ia-factory-01"
  hostname     = "tenant-template"
  ostemplate   = "local:vztmpl/debian-12-standard_12.0-1_amd64.tar.zst"
  unprivileged = true
  
  rootfs {
    storage = "local-lvm"
    size    = "50G"
  }
  
  network {
    name   = "eth0"
    bridge = "vmbr0"
    ip     = "dhcp"
  }
  
  features {
    nesting = true
  }
}

# Module for creating tenant containers
module "tenant" {
  source = "./modules/tenant"
  
  for_each = var.tenants
  
  tenant_id   = each.key
  tier        = each.value.tier
  cpu_cores   = each.value.cpu_cores
  ram_mb      = each.value.ram_mb
  disk_gb     = each.value.disk_gb
  target_node = each.value.node
}
"""


# Instance globale
infra_manager = MultiTenantManager()


# ===== API ROUTES =====

@router.post("/tenants", response_model=Dict[str, Any])
async def create_tenant(request: TenantRequest, background_tasks: BackgroundTasks):
    """Crée un nouveau tenant"""
    try:
        tenant = await infra_manager.create_tenant(request)
        return {
            "status": "success",
            "tenant_id": tenant.id,
            "region": tenant.region.value,
            "tier": tenant.tier.value,
            "resources": tenant.resources,
            "url": f"https://{tenant.custom_domain or f'{tenant.id}.iafactory.ch'}",
            "status": tenant.status.value
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tenants/{tenant_id}")
async def get_tenant(tenant_id: str):
    """Récupère un tenant par ID"""
    tenant = infra_manager.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.get("/tenants")
async def list_tenants(
    region: Optional[Region] = None,
    tier: Optional[TenantTier] = None,
    status: Optional[TenantStatus] = None
):
    """Liste tous les tenants"""
    return infra_manager.list_tenants(region, tier, status)


@router.post("/tenants/{tenant_id}/suspend")
async def suspend_tenant(tenant_id: str):
    """Suspend un tenant"""
    try:
        await infra_manager.suspend_tenant(tenant_id)
        return {"status": "suspended", "tenant_id": tenant_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tenants/{tenant_id}/terminate")
async def terminate_tenant(tenant_id: str):
    """Termine un tenant"""
    try:
        await infra_manager.terminate_tenant(tenant_id)
        return {"status": "terminated", "tenant_id": tenant_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/metrics")
async def get_infrastructure_metrics():
    """Retourne les métriques d'infrastructure"""
    return infra_manager.get_infrastructure_metrics()


@router.get("/servers")
async def list_servers():
    """Liste tous les serveurs"""
    return list(infra_manager.servers.values())


@router.get("/servers/{server_id}")
async def get_server(server_id: str):
    """Récupère un serveur par ID"""
    server = infra_manager.servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server


@router.get("/pricing")
async def get_pricing():
    """Retourne la grille tarifaire"""
    return {
        tier.value: {
            "resources": resources,
            "features": [
                f"{resources['cpu_cores']} CPU cores",
                f"{resources['ram_gb']} GB RAM",
                f"{resources['disk_gb']} GB SSD",
                f"{resources['concurrent_users']} utilisateurs simultanés",
                f"{resources['api_calls_month']:,} appels API/mois"
            ]
        }
        for tier, resources in TIER_RESOURCES.items()
    }


@router.get("/config/proxmox")
async def get_proxmox_config():
    """Génère la configuration Proxmox"""
    return {
        "config": infra_manager.generate_proxmox_config(),
        "format": "proxmox-ve"
    }


@router.get("/config/terraform")
async def get_terraform_config():
    """Génère la configuration Terraform"""
    return {
        "config": infra_manager.generate_terraform_config(),
        "format": "hcl"
    }
