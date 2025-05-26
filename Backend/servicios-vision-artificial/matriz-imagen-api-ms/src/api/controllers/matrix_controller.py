"""
Controlador para la conversión de matrices a imágenes.
"""
import io
import json
from fastapi import HTTPException, UploadFile, File, Form, Body
from fastapi.responses import Response
from typing import Optional, Dict, Any, Union

from src.services.matrix_service import MatrixService
from src.utils.validation import validate_matrix_data
import httpx
import base64

class MatrixController:
    @staticmethod
    async def convert_matrix(
        data: Union[Dict[str, Any], bytes, str], 
        format: str, 
        output_format: str = "png"
    ):
        """
        Controla el flujo de conversión de matriz a imagen.
        
        Args:
            data: Datos de la matriz
            format: Formato de entrada ('json' o 'numpy')
            output_format: Formato de salida de la imagen ('png', 'jpeg', etc.)
            
        Returns:
            Response con la imagen generada
        """
        # Validar datos
        await validate_matrix_data(data, format)
        
        try:
            # Convertir matriz a imagen
            img_bytes, content_type = await MatrixService.matrix_to_image(
                data, format, output_format
            )
            
            # Devolver la imagen
            return Response(content=img_bytes, media_type=content_type)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al convertir la matriz a imagen: {str(e)}"
            )
    
    @staticmethod
    async def generate_comparison(
        matrix_data: Dict[str, Any], 
        original_image: UploadFile,
        format: str, 
        preprocess: Optional[str] = None
    ):
        """
        Genera una comparación entre la imagen original y la reconstruida.
        
        Args:
            matrix_data: Datos de la matriz
            original_image: Archivo de imagen original
            format: Formato de los datos de matriz ('json' o 'numpy')
            preprocess: Opciones de preprocesamiento aplicadas
            
        Returns:
            Response con la imagen de comparación
        """
        # Validar datos
        await validate_matrix_data(matrix_data, format)
        
        try:
            # Leer la imagen original
            original_img_bytes = await original_image.read()
            
            # Convertir la matriz a imagen
            reconstructed_img_bytes, _ = await MatrixService.matrix_to_image(
                matrix_data, format, "png"
            )
            
            # Generar la comparación
            comparison_img_bytes = await MatrixService.generate_comparison_image(
                original_img_bytes, reconstructed_img_bytes
            )
            
            # Devolver la imagen de comparación
            return Response(content=comparison_img_bytes, media_type="image/png")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar la comparación: {str(e)}"
            )
    
    @staticmethod
    async def verify_transformation(
        original_image: UploadFile,
        preprocess: Optional[str] = None,
        api_key: str = None
    ):
        """
        Verifica la transformación completa: imagen → matriz → imagen
        
        Args:
            original_image: Archivo de imagen original
            preprocess: Opciones de preprocesamiento (opcional)
            api_key: Clave API para el servicio ImageToMatrix
            
        Returns:
            Response con la imagen de comparación
        """
        from src.config.settings import get_settings
        settings = get_settings()
        
        try:
            # 1. Guardar la imagen original para usarla después
            original_bytes = await original_image.read()
            await original_image.seek(0)  # Rebobinar para reutilizar
            
            # 2. Enviar la imagen al servicio ImageToMatrix para obtener la matriz
            headers = {"X-API-Key": api_key or settings.DEFAULT_API_KEY}
            
            # Crear el formulario para la petición
            form_data = {"image": original_image, "format": "json"}
            if preprocess:
                form_data["preprocess"] = preprocess
            
            # Realizar petición HTTP al servicio ImageToMatrix
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.IMAGE_TO_MATRIX_URL,
                    files={"image": (original_image.filename, original_bytes, original_image.content_type)},
                    data={"format": "json", "preprocess": preprocess},
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error en ImageToMatrix: {response.text}"
                    )
                
                # Obtener la matriz desde la respuesta
                matrix_data = response.json()
            
            # 3. Convertir la matriz de vuelta a imagen
            reconstructed_img_bytes, _ = await MatrixService.matrix_to_image(
                matrix_data, "json", "png"
            )
            
            # 4. Generar y devolver la imagen de comparación
            comparison_img_bytes = await MatrixService.generate_comparison_image(
                original_bytes, reconstructed_img_bytes
            )
            
            return Response(content=comparison_img_bytes, media_type="image/png")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al verificar la transformación: {str(e)}"
            )
