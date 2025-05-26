"""
Utilidades para validación de datos.
"""
from fastapi import HTTPException
import json
from typing import Dict, Any, Union

from src.config.settings import get_settings

settings = get_settings()

async def validate_matrix_data(data: Union[Dict[str, Any], bytes], format: str):
    """
    Valida que los datos de la matriz sean válidos.
    
    Args:
        data: Datos de la matriz a validar
        format: Formato de los datos ('json' o 'numpy')
        
    Raises:
        HTTPException: Si los datos no son válidos
    """
    # Verificar que hay datos
    if not data:
        raise HTTPException(
            status_code=400,
            detail="No se han proporcionado datos de matriz"
        )
    
    # Verificar formato
    if format.lower() not in settings.ALLOWED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no compatible. Formatos permitidos: {', '.join(settings.ALLOWED_FORMATS)}"
        )
    
    # Validación específica para formato JSON
    if format.lower() == "json":
        try:
            # Si es un diccionario ya parseado
            if isinstance(data, dict):
                if "matrix" not in data:
                    raise HTTPException(
                        status_code=400,
                        detail="El objeto JSON debe contener la clave 'matrix'"
                    )
            # Si son bytes o string
            else:
                # Intentar parsear JSON
                json_data = json.loads(data) if isinstance(data, str) or isinstance(data, bytes) else None
                if not json_data or "matrix" not in json_data:
                    raise HTTPException(
                        status_code=400,
                        detail="El objeto JSON debe contener la clave 'matrix'"
                    )
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="JSON inválido"
            )
    
    # Para numpy, la validación se hará durante el procesamiento debido a su naturaleza binaria
