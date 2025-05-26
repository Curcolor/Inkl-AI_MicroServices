"""
Pruebas de integración para los endpoints de la API.
"""
import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image
import numpy as np

from src.api.app import app
from src.config.settings import get_settings

settings = get_settings()
client = TestClient(app)

@pytest.fixture
def test_image():
    """Crea una imagen de prueba."""
    img = Image.new('RGB', (100, 100), color='blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def test_health_endpoint():
    """Prueba el endpoint de salud."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_convert_endpoint(test_image):
    """Prueba el endpoint de conversión de imagen a matriz."""
    # Preparar los datos
    files = {
        'image': ('test.png', test_image, 'image/png')
    }
    data = {
        'format': 'json',
        'preprocess': ['grayscale']
    }
    headers = {
        settings.API_KEY_HEADER: settings.DEFAULT_API_KEY
    }
    
    # Hacer la petición
    response = client.post(
        "/api/v1/convert",
        files=files,
        data=data,
        headers=headers
    )
    
    # Verificar respuesta
    assert response.status_code == 200
    result = response.json()
    
    # Verificar que contiene una matriz y los metadatos
    assert "matrix" in result
    assert "shape" in result
    assert "dtype" in result
    
    # Verificar dimensiones (debe ser una imagen en escala de grises)
    assert len(result["shape"]) == 2  # Escala de grises, no debería tener canal de color

def test_convert_endpoint_unauthorized(test_image):
    """Prueba el endpoint sin API key."""
    files = {
        'image': ('test.png', test_image, 'image/png')
    }
    data = {
        'format': 'json'
    }
    
    response = client.post(
        "/api/v1/convert",
        files=files,
        data=data
    )
    
    assert response.status_code == 401
