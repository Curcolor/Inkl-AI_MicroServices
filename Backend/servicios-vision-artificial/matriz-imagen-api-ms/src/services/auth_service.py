"""
Servicio de autenticación para la API.
"""
from fastapi import Header, HTTPException, Depends
from typing import Optional

from src.config.settings import get_settings

settings = get_settings()

async def verify_api_key(
    api_key: Optional[str] = Header(None, alias=settings.API_KEY_HEADER)
):
    """
    Verifica la clave API proporcionada.
    
    Args:
        api_key: Clave API en la cabecera
        
    Returns:
        La clave API si es válida
        
    Raises:
        HTTPException: Si la clave API es inválida o faltante
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )
        
    # En un entorno de producción, esto sería una comparación con claves
    # almacenadas de forma segura (base de datos, servicio de secretos, etc.)
    if api_key != settings.DEFAULT_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
        
    return api_key
