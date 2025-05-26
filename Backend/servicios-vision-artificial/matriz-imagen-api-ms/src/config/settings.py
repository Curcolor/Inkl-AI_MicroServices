"""
Configuraciones de la aplicación.
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Servidor
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001  # Usando puerto 8001 para evitar conflicto con ImageToMatrix
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Límites y parámetros
    MAX_MATRIX_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_FORMATS: List[str] = ["json", "numpy"]
    
    # Seguridad
    API_KEY_HEADER: str = "X-API-Key"
    DEFAULT_API_KEY: str = "development_key_change_me"

    # URL del servicio de ImageToMatrix
    IMAGE_TO_MATRIX_URL: str = "http://localhost:8000/api/v1/convert"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

@lru_cache()
def get_settings() -> Settings:
    """
    Carga las configuraciones desde variables de entorno o archivo .env
    con caché LRU para optimizar el rendimiento.
    
    Returns:
        Objeto Settings con la configuración
    """
    return Settings()
