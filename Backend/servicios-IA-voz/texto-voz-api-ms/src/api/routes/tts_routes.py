"""
Rutas para la API de texto a voz.
"""
from fastapi import APIRouter, Body
from typing import Dict, Any

from src.api.controllers.tts_controller import TTSController

router = APIRouter(tags=["TTS"])

@router.get("/estado", summary="Verificar estado del servicio")
async def verificar_estado():
    """
    Verifica el estado actual del servicio TTS.
    """
    return TTSController.verificar_estado()

@router.get("/voces", summary="Obtener información sobre voces")
async def obtener_voces():
    """
    Esta ruta ahora solo devuelve información instructiva sobre cómo usar las voces del navegador.
    """
    return TTSController.obtener_voces()
