from prometheus_client import Histogram, Counter, Gauge
import logging

logger = logging.getLogger(__name__)

# Métriques Prometheus
REQ_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency by route',
    ['method', 'route']
)

REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total requests by route and status',
    ['method', 'route', 'status_code']
)

QUOTA_USAGE = Gauge(
    'quota_usage_ratio',
    'Quota usage ratio by tenant and resource',
    ['tenant_id', 'resource_type']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections_total',
    'Number of active connections'
)

def init_metrics():
    """Initialize monitoring system"""
    logger.info("Prometheus metrics initialized")
