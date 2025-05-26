"""
Tests para el controlador TTS.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.api.controllers.tts_controller import TTSController

class TestTTSController:
    """
    Clase para probar el controlador TTS.
    """
    
    def test_verificar_estado(self):
        """Test para el método verificar_estado."""
        resultado = TTSController.verificar_estado()
        
        assert isinstance(resultado, dict)
        assert "estado" in resultado
        assert resultado["estado"] == "operativo"
        assert "mensaje" in resultado
        assert "modo" in resultado
        assert "timestamp" in resultado
    
    def test_obtener_voces(self):
        """Test para el método obtener_voces."""
        resultado = TTSController.obtener_voces()
        
        assert isinstance(resultado, dict)
        assert "mensaje" in resultado
        assert "info" in resultado
        assert "documentacion" in resultado
        assert "timestamp" in resultado
