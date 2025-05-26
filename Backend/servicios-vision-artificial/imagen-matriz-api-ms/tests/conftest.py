"""
Configuración para pruebas con pytest.
"""
import pytest
import os
import sys

# Asegurar que el directorio raíz del proyecto está en PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración para pruebas
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Configura el entorno para las pruebas.
    """
    # Establecer variables de entorno para pruebas
    os.environ["DEBUG"] = "True"
    os.environ["API_PORT"] = "8001"  # Puerto diferente para pruebas
    os.environ["DEFAULT_API_KEY"] = "test_api_key"
    
    yield
    
    # Limpiar después de las pruebas
    os.environ.pop("DEBUG", None)
    os.environ.pop("API_PORT", None)
    os.environ.pop("DEFAULT_API_KEY", None)
