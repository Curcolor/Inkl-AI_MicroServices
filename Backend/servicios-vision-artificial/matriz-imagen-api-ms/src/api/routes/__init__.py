"""
Rutas de la API para la conversión de matrices a imágenes.
"""
from fastapi import APIRouter, UploadFile, File, Form, Body, Depends, HTTPException
from fastapi.responses import Response
from typing import Optional, Dict, Any, List

from src.api.controllers.matrix_controller import MatrixController
from src.services.auth_service import verify_api_key

router = APIRouter(tags=["Matrix Conversion"])

@router.post("/convert", summary="Convertir matriz a imagen")
async def convert_matrix_to_image(
    matrix: Dict[str, Any] = Body(...),
    format: str = Form("json"),
    output_format: str = Form("png"),
    api_key: str = Depends(verify_api_key)
):
    """
    Convierte una matriz numérica a una imagen.
    
    - **matrix**: Datos de la matriz en formato JSON
    - **format**: Formato de entrada de la matriz (json, numpy)
    - **output_format**: Formato de salida de la imagen (png, jpeg, etc.)
    """
    try:
        return await MatrixController.convert_matrix(matrix, format, output_format)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify", summary="Verificar transformación imagen-matriz-imagen")
async def verify_transformation(
    image: UploadFile = File(...),
    preprocess: Optional[str] = Form(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Verifica la transformación completa: imagen → matriz → imagen.
    Muestra una comparación entre la imagen original y la reconstruida.
    
    - **image**: Archivo de imagen a procesar
    - **preprocess**: Opciones de preprocesamiento separadas por comas
    """
    try:
        return await MatrixController.verify_transformation(image, preprocess, api_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compare", summary="Comparar imagen original con reconstruida")
async def compare_images(
    matrix: Dict[str, Any] = Body(...),
    original_image: UploadFile = File(...),
    format: str = Form("json"),
    preprocess: Optional[str] = Form(None),
    api_key: str = Depends(verify_api_key)
):
    """
    Genera una comparación entre la imagen original y la reconstruida desde la matriz.
    
    - **matrix**: Datos de la matriz en formato JSON
    - **original_image**: Archivo de imagen original
    - **format**: Formato de entrada de la matriz (json, numpy)
    - **preprocess**: Opciones de preprocesamiento aplicadas (opcional)
    """
    try:
        return await MatrixController.generate_comparison(matrix, original_image, format, preprocess)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))