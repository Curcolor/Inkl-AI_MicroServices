"""
Modelos de datos para la API de DeepSeek.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any

class ProcesamientoRequest(BaseModel):
    """
    Modelo para la solicitud de procesamiento de texto.
    """
    texto: str = Field(..., description="Texto a procesar por el modelo de DeepSeek")
    temperatura: Optional[float] = Field(None, description="Nivel de aleatoriedad en la generación (0.0 a 1.0)")
    max_tokens: Optional[int] = Field(None, description="Número máximo de tokens a generar")
    modelo: Optional[str] = Field(None, description="Modelo de DeepSeek a utilizar")
    
    @validator('texto')
    def texto_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('El texto no puede estar vacío')
        return v
    
    @validator('temperatura')
    def temperatura_valida(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('La temperatura debe estar entre 0.0 y 1.0')
        return v
    
    @validator('max_tokens')
    def max_tokens_valido(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El número máximo de tokens debe ser mayor que 0')
        return v

class ProcesamientoResponse(BaseModel):
    """
    Modelo para la respuesta de procesamiento de texto.
    """
    texto_procesado: str = Field(..., description="Texto procesado por el modelo")
    modelo_usado: str = Field(..., description="Modelo utilizado para el procesamiento")
    tokens_entrada: int = Field(..., description="Número de tokens en el texto de entrada")
    tokens_salida: int = Field(..., description="Número de tokens generados")
    tiempo_proceso: float = Field(..., description="Tiempo de proceso en segundos")

class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error.
    """
    error: str = Field(..., description="Descripción del error")
    detalle: Optional[str] = Field(None, description="Detalle adicional sobre el error")
    codigo: int = Field(..., description="Código HTTP del error")
