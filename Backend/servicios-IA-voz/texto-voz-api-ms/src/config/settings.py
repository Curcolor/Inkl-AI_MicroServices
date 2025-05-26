"""
Configuraciones de la aplicación.
"""
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    # Servidor
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.getenv('API_PORT'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Seguridad
    TTS_API_Key: str = os.getenv('TTS_API_Key')
    
    # TTS
    CLIENT_SIDE_PROCESSING: bool = True
    TTS_ENGINE: str = "Web Speech API"
    
    # Límites
    MAX_TEXT_LENGTH: int = int(os.getenv('MAX_TEXT_LENGTH'))
    
    # Configuración de audio
    DEFAULT_VOICE_RATE: int = int(os.getenv('DEFAULT_VOICE_RATE'))
    DEFAULT_VOICE_VOLUME: float = float(os.getenv('DEFAULT_VOICE_VOLUME'))
    AUDIO_OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'audio')
    
    model_config = {
        "env_file": ".env",
        "env_prefix": "",
        "extra": "ignore"  # Ignorar variables de entorno adicionales
    }

@lru_cache()
def get_settings() -> Settings:
    """
    Carga las configuraciones desde variables de entorno o archivo .env
    con caché LRU para optimizar el rendimiento.
    
    Returns:
        Objeto Settings con la configuración
    """
    settings = Settings()
    return settings
