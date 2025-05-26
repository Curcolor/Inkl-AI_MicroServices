"""
Modelos de solicitud para la API de texto a voz.
"""
from pydantic import BaseModel, Field
from typing import Optional
from ...config.settings import get_settings

settings = get_settings()

class TextoAVozRequest(BaseModel):
    """Modelo para solicitudes de conversión de texto a voz."""
    texto: str = Field(..., description="Texto a convertir en voz")
    velocidad: Optional[int] = Field(None, description="Velocidad de habla (1-100)")
    volumen: Optional[float] = Field(None, description="Volumen de habla (0.0-1.0)")
      class Config:
        json_schema_extra = {
            "example": {
                "texto": "Hola, este es un ejemplo de conversión de texto a voz",
                "velocidad": settings.VELOCIDAD_PREDETERMINADA,
                "volumen": settings.VOLUMEN_PREDETERMINADO
            }
        }
