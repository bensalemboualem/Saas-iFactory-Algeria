"""
API v1 Router
Aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import translator
# Import other endpoints as you create them
# from app.api.v1.endpoints import speech_to_text, text_generator, image_generator, etc.

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(translator.router)

# Add more routers as you implement them:
# api_router.include_router(speech_to_text.router)
# api_router.include_router(text_generator.router)
# api_router.include_router(image_generator.router)
# api_router.include_router(background_remover.router)
# api_router.include_router(image_upscaler.router)
# api_router.include_router(image_transformer.router)
