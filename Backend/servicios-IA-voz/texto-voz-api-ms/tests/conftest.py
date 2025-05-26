"""
Configuración para pytest.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Añadir el directorio raíz al path para permitir importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cargar variables de entorno de prueba
os.environ["API_HOST"] = "0.0.0.0"
os.environ["API_PORT"] = "5002"
os.environ["DEBUG"] = "False"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["TTS_API_Key"] = "test_tts_api_key"
os.environ["MAX_TEXT_LENGTH"] = "1000"
os.environ["DEFAULT_VOICE_RATE"] = "1"
os.environ["DEFAULT_VOICE_VOLUME"] = "1.0"

@pytest.fixture
def client():
    """
    Fixture para crear un cliente de prueba para la API.
    """
    from src.api.app import app
    return TestClient(app)
