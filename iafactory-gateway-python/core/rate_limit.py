# -*- coding: utf-8 -*-
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from collections import defaultdict

# Simple in-memory rate limiter
rate_limits = defaultdict(list)
MAX_REQUESTS = 60
TIME_WINDOW = 60  # secondes

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = datetime.now()
    
    # Nettoie vieilles requêtes
    rate_limits[client_ip] = [t for t in rate_limits[client_ip] if now - t < timedelta(seconds=TIME_WINDOW)]
    
    # Check limit
    if len(rate_limits[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    rate_limits[client_ip].append(now)
    return await call_next(request)
