"""
Módulo de configuración para la aplicación.
Todas las configuraciones se obtienen de variables de entorno.
"""
import os
from pydantic_settings import BaseSettings
from typing import List, Set

class Configuracion(BaseSettings):
    """Configuración de la aplicación."""
    # Motor de transcripción
    motor_transcripcion: str
    api_clave: str = ""  # Puede estar vacío para motor local
    
    # Configuración del servidor
    api_host: str
    api_puerto: int
    
    # Configuración de logging
    nivel_log: str
    
    # Configuración de archivos de audio
    tamano_max_archivo: int  # En MB
    formatos_permitidos: str
    tiempo_espera: int  # En segundos
    
    @property
    def formatos_permitidos_lista(self) -> List[str]:
        """Devuelve la lista de formatos permitidos como lista."""
        return self.formatos_permitidos.lower().split(',')
    
    @property
    def formatos_permitidos_set(self) -> Set[str]:
        """Devuelve la lista de formatos permitidos como conjunto para búsquedas más eficientes."""
        return set(self.formatos_permitidos_lista)
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }

# Inicializar configuración
try:
    configuracion = Configuracion()
except Exception as e:
    # Proporcionar valores predeterminados si la carga de variables de entorno falla
    print(f"Error al cargar la configuración: {e}")
    print("Utilizando valores predeterminados...")
    configuracion = Configuracion(
        motor_transcripcion=os.getenv("MOTOR_TRANSCRIPCION", "local"),
        api_clave=os.getenv("API_CLAVE", ""),
        api_host=os.getenv("API_HOST", "0.0.0.0"),
        api_puerto=int(os.getenv("API_PUERTO", "5003")),
        nivel_log=os.getenv("NIVEL_LOG", "INFO"),
        tamano_max_archivo=int(os.getenv("TAMANO_MAX_ARCHIVO", "10")),
        formatos_permitidos=os.getenv("FORMATOS_PERMITIDOS", "wav,mp3,ogg,webm"),
        tiempo_espera=int(os.getenv("TIEMPO_ESPERA", "30"))
    )
