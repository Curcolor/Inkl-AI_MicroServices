"""
Archivo de configuración para las pruebas.
"""
import os
import sys
import pytest
from dotenv import load_dotenv

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar variables de entorno para pruebas
load_dotenv("tests/.env.test")

@pytest.fixture
def test_configuracion():
    """Fixture para la configuración de prueba."""
    from src.config import Configuracion
    
    return Configuracion(
        motor_transcripcion="local",
        api_clave="",
        api_host="localhost",
        api_puerto=8000,
        nivel_log="DEBUG",
        tamano_max_archivo=10,
        formatos_permitidos="wav,mp3,ogg,webm",
        tiempo_espera=30
    )

@pytest.fixture
def cliente_prueba():
    """Fixture para el cliente de prueba."""
    from fastapi.testclient import TestClient
    from src.api.app import app
    
    return TestClient(app)
