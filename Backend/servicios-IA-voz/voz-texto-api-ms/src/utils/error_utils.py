"""
Módulo de utilidades para el manejo de errores en la aplicación.
"""
from typing import Dict, Any, Optional

class ErrorBase(Exception):
    """Clase base para errores personalizados de la aplicación."""
    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el error a un diccionario."""
        return {"error": self.__class__.__name__, "detalle": self.mensaje}

class ErrorFormatoAudio(ErrorBase):
    """Error cuando el formato del archivo de audio no es soportado."""
    pass

class ErrorTamanoArchivo(ErrorBase):
    """Error cuando el archivo de audio excede el tamaño máximo permitido."""
    pass

class ErrorTranscripcion(ErrorBase):
    """Error durante el proceso de transcripción."""
    pass

class ErrorMotorTranscripcion(ErrorBase):
    """Error relacionado con el motor de transcripción."""
    pass

class ErrorProcesamiento(ErrorBase):
    """Error durante el procesamiento del archivo de audio."""
    pass

def crear_respuesta_error(
    codigo_estado: int, 
    tipo_error: str, 
    mensaje: str, 
    detalle: Optional[str] = None
) -> Dict[str, Any]:
    """
    Crea una respuesta de error consistente.
    
    Args:
        codigo_estado: Código HTTP del error
        tipo_error: Tipo de error
        mensaje: Mensaje de error
        detalle: Detalles adicionales del error (opcional)
        
    Returns:
        Diccionario con la información del error
    """
    respuesta = {
        "error": tipo_error,
        "mensaje": mensaje,
        "codigo": codigo_estado
    }
    
    if detalle:
        respuesta["detalle"] = detalle
        
    return respuesta
