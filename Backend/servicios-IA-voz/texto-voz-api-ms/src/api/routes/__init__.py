"""
Inicialización del paquete de rutas.

Define el router principal que incluye todas las subrutas.
"""
from fastapi import APIRouter

from src.api.routes.tts_routes import router as tts_router

# Crear router principal
router = APIRouter()

# Incluir todos los routers
router.include_router(tts_router, prefix="/tts")
