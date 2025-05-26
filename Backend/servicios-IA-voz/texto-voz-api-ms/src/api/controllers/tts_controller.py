"""
Controlador para la API de texto a voz.
"""
import time
from fastapi import HTTPException
from typing import Dict, Any, Optional

from src.config.settings import get_settings

settings = get_settings()

class TTSController:
    """Controlador para las operaciones de texto a voz."""
    
    @staticmethod
    def verificar_estado() -> Dict[str, Any]:
        """
        Verifica el estado del servicio TTS.
        
        Returns:
            Dict con información del estado del servicio
        """
        return {
            'estado': 'operativo',
            'mensaje': 'El servicio de texto a voz está funcionando correctamente',
            'modo': 'cliente',
            'info': 'Este servicio ahora opera principalmente en el navegador del cliente',
            'max_texto': settings.MAX_TEXT_LENGTH,
            'timestamp': time.time()
        }
    
    @staticmethod
    def obtener_voces() -> Dict[str, Any]:
        """
        Obtiene información sobre las voces disponibles.
        
        Returns:
            Dict con información sobre cómo usar las voces del navegador
        """
        return {
            'mensaje': 'Las voces ahora se obtienen directamente del navegador usando la Web Speech API',
            'info': 'Para acceder a las voces use: window.speechSynthesis.getVoices() en el cliente',
            'documentacion': 'https://developer.mozilla.org/es/docs/Web/API/Web_Speech_API',
            'timestamp': time.time()
        }
