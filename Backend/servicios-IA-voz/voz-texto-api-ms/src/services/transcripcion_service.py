"""
Servicio principal para la transcripción de voz a texto.
"""
from typing import Dict, Any, Optional

from ..config import configuracion
from ..utils import ErrorTranscripcion, ErrorMotorTranscripcion
from .motores_transcripcion import (
    MotorTranscripcionBase,
    MotorTranscripcionLocal,
    MotorTranscripcionGoogle
)

class ServicioTranscripcion:
    """Servicio para transcribir audio a texto."""
    
    def __init__(self, configuracion_servicio: Any = None):
        """
        Inicializa el servicio con la configuración especificada.
        
        Args:
            configuracion_servicio: Configuración del servicio (opcional)
                Si no se proporciona, se utilizará la configuración global
        """
        self.configuracion = configuracion_servicio or configuracion
        self.motor = self._inicializar_motor()
    
    def _inicializar_motor(self) -> MotorTranscripcionBase:
        """
        Inicializa el motor de transcripción según la configuración.
        
        Returns:
            Motor de transcripción inicializado
            
        Raises:
            ErrorMotorTranscripcion: Si el motor de transcripción no es soportado
        """
        motor_nombre = self.configuracion.motor_transcripcion.lower()
        
        if motor_nombre == "local":
            return MotorTranscripcionLocal()
        elif motor_nombre == "google":
            return MotorTranscripcionGoogle(self.configuracion.api_clave)
        # Añadir más motores según sea necesario
        else:
            raise ErrorMotorTranscripcion(
                f"Motor de transcripción no soportado: {motor_nombre}"
            )
    
    def transcribir(self, ruta_archivo: str, opciones: Optional[Dict[str, Any]] = None) -> str:
        """
        Transcribe un archivo de audio a texto.
        
        Args:
            ruta_archivo: Ruta al archivo de audio
            opciones: Opciones adicionales para la transcripción
            
        Returns:
            Texto transcrito
            
        Raises:
            ErrorTranscripcion: Si ocurre un error durante la transcripción
        """
        try:
            return self.motor.transcribir(ruta_archivo, opciones)
        except Exception as e:
            if isinstance(e, ErrorTranscripcion):
                raise e
            else:
                raise ErrorTranscripcion(f"Error al transcribir audio: {str(e)}")

# Instancia global del servicio
servicio_transcripcion = ServicioTranscripcion(configuracion)
