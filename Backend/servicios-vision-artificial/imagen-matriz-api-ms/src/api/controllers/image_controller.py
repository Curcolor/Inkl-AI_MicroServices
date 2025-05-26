"""
Controlador para la conversión de imágenes a matrices.
"""
from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
import numpy as np
import io

from src.services.image_service import ImageService
from src.utils.validation import validate_image

class ImageController:
    @staticmethod
    async def convert_image(
        image: UploadFile, 
        format: str = "json", 
        preprocess: Optional[List[str]] = None
    ):
        """
        Controla el flujo de conversión de una imagen a matriz.
        
        Args:
            image: Archivo de imagen subido
            format: Formato de salida (json, numpy)
            preprocess: Lista de operaciones de preprocesamiento
            
        Returns:
            JSONResponse con la matriz o respuesta binaria según el formato
        """
        # Validar imagen
        await validate_image(image)
        
        # Leer contenido de la imagen
        content = await image.read()
        image_bytes = io.BytesIO(content)
        
        # Convertir a matriz usando el servicio
        try:
            matrix = await ImageService.image_to_matrix(image_bytes, preprocess)
            
            # Devolver en el formato solicitado
            if format.lower() == "json":
                return JSONResponse(
                    content={
                        "matrix": matrix.tolist(),
                        "shape": matrix.shape,
                        "dtype": str(matrix.dtype)
                    }
                )
            elif format.lower() == "numpy":
                output = io.BytesIO()
                np.save(output, matrix)
                output.seek(0)
                return output.getvalue()
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Formato no soportado: {format}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar la imagen: {str(e)}"
            )
