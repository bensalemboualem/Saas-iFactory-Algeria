import time
import hashlib
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from .db import get_tenant_by_key, insert_usage

logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = hashlib.sha256(str(time.time_ns()).encode()).hexdigest()[:16]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Autoriser les requêtes OPTIONS pour CORS
        if request.method == "OPTIONS":
            return await call_next(request)
            
        # Routes publiques
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json", "/"]:
            return await call_next(request)
        
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization", "").replace("Bearer ", "")
        if not api_key:
            return JSONResponse({"error": "API key required"}, status_code=401)
        
        tenant = get_tenant_by_key(api_key)
        if not tenant:
            return JSONResponse({"error": "Invalid API key"}, status_code=401)
        
        request.state.tenant = tenant
        
        start_time = time.time()
        response = await call_next(request)
        latency_ms = int((time.time() - start_time) * 1000)
        
        try:
            insert_usage({
                "tenant_id": tenant["id"],
                "request_id": request.state.request_id,
                "route": request.url.path,
                "method": request.method,
                "latency_ms": latency_ms,
                "status_code": response.status_code
            })
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
        
        return response
