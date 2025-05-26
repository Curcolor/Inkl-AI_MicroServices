"""
Prueba unitaria para el servicio de conversión de imagen a matriz.
"""
import pytest
import numpy as np
from io import BytesIO
from PIL import Image
import os
import sys

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.image_service import ImageService

@pytest.fixture
def sample_image_bytes():
    """Crea una imagen de muestra para las pruebas."""
    # Crear una imagen 10x10 con valores aleatorios
    img = Image.new('RGB', (10, 10), color='red')
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return byte_io

@pytest.mark.asyncio
async def test_image_to_matrix(sample_image_bytes):
    """Prueba la conversión básica de imagen a matriz."""
    matrix = await ImageService.image_to_matrix(sample_image_bytes)
    
    # Verificar que es una matriz numpy con la forma correcta
    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (10, 10, 3)
    
    # Verificar que es una imagen roja (todos los pixels son rojos)
    assert np.all(matrix[:, :, 0] == 255)  # Canal R
    assert np.all(matrix[:, :, 1] == 0)    # Canal G
    assert np.all(matrix[:, :, 2] == 0)    # Canal B

@pytest.mark.asyncio
async def test_grayscale_preprocessing(sample_image_bytes):
    """Prueba el preprocesamiento a escala de grises."""
    matrix = await ImageService.image_to_matrix(sample_image_bytes, ["grayscale"])
    
    # Verificar que es una matriz con un solo canal
    assert len(matrix.shape) == 2 or matrix.shape[2] == 1
