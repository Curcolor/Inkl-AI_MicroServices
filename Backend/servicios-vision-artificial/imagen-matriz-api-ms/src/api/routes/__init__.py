"""
Rutas de la API para la conversión de imágenes a matrices.
"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List

from src.api.controllers.image_controller import ImageController
from src.services.auth_service import verify_api_key

router = APIRouter(tags=["Image Conversion"])

@router.post("/convert", summary="Convertir imagen a matriz")
async def convert_image_to_matrix(
    image: UploadFile = File(...),
    format: str = Form("json"),
    preprocess: Optional[List[str]] = Form(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Convierte una imagen a una matriz numérica.
    
    - **image**: Archivo de imagen a convertir
    - **format**: Formato de salida (json, numpy)
    - **preprocess**: Opciones de preprocesamiento (resize, normalize, grayscale)
    """
    try:
        return await ImageController.convert_image(image, format, preprocess)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
