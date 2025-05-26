"""
Utilidades para validación de datos.
"""
from fastapi import UploadFile, HTTPException
from typing import List

from src.config.settings import get_settings

settings = get_settings()

async def validate_image(image: UploadFile):
    """
    Valida que el archivo subido sea una imagen válida.
    
    Args:
        image: Archivo de imagen a validar
        
    Raises:
        HTTPException: Si la imagen no es válida
    """
    # Verificar que el archivo existe
    if not image:
        raise HTTPException(
            status_code=400,
            detail="No se ha proporcionado ninguna imagen"
        )
    
    # Verificar el tamaño del archivo
    content = await image.read()
    await image.seek(0)  # Rebobinar el archivo para lecturas futuras
    
    if len(content) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"El tamaño de la imagen excede el límite de {settings.MAX_IMAGE_SIZE/1024/1024} MB"
        )
    
    # Verificar la extensión del archivo
    extension = image.filename.split(".")[-1].lower() if image.filename else ""
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato de imagen no compatible. Formatos permitidos: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Verificar el tipo MIME
    content_type = image.content_type
    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="El archivo proporcionado no es una imagen válida"
        )
