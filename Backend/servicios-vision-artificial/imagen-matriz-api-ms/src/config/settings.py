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
    API_PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Límites y parámetros
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "bmp", "tiff"]
    MAX_WIDTH: int = 2048
    MAX_HEIGHT: int = 2048
      # Seguridad
    API_KEY_HEADER: str = "DEFAULT_API_KEY"
    DEFAULT_API_KEY: str = os.getenv("DEFAULT_API_KEY")
    
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
