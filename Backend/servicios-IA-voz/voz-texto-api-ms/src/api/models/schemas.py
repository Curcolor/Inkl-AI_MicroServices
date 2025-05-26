"""
Modelos Pydantic para la API de transcripción de voz a texto.
"""
from pydantic import BaseModel, Field
from typing import Optional

class RespuestaTranscripcion(BaseModel):
    """Modelo para la respuesta de transcripción."""
    texto: str = Field(..., description="Texto transcrito del audio")
    confianza: Optional[float] = Field(None, description="Nivel de confianza de la transcripción (0-1)")
    idioma_detectado: Optional[str] = Field(None, description="Idioma detectado en el audio")
    duracion: Optional[float] = Field(None, description="Duración del audio en segundos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "texto": "Este es un ejemplo de texto transcrito del audio.",
                "confianza": 0.95,
                "idioma_detectado": "es-ES",
                "duracion": 5.2
            }
        }

class EstadoSalud(BaseModel):
    """Modelo para la respuesta del endpoint de salud."""
    estado: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión del servicio")
    motor_transcripcion: str = Field(..., description="Motor de transcripción activo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado": "en línea",
                "version": "1.0.0",
                "motor_transcripcion": "local"
            }
        }

class OpcionesTranscripcion(BaseModel):
    """Modelo para las opciones adicionales de transcripción."""
    idioma: Optional[str] = Field(None, description="Código de idioma (ej: es-ES, en-US)")
    modelo: Optional[str] = Field(None, description="Modelo específico a utilizar")
    sensibilidad: Optional[float] = Field(None, ge=0, le=1, description="Sensibilidad del reconocimiento (0-1)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "idioma": "es-ES",
                "modelo": "general",
                "sensibilidad": 0.8
            }
        }
