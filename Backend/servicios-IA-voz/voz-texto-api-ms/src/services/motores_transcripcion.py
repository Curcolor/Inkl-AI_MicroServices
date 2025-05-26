"""
Implementación de diferentes motores de transcripción de voz a texto.
"""
import os
import time
import speech_recognition as sr
import requests
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from src.config import configuracion
from src.utils import ErrorMotorTranscripcion, ErrorTranscripcion

class MotorTranscripcionBase(ABC):
    """Clase base para motores de transcripción."""
    
    @abstractmethod
    def transcribir(self, ruta_archivo: str, opciones: Optional[Dict[str, Any]] = None) -> str:
        """
        Transcribe un archivo de audio a texto.
        
        Args:
            ruta_archivo: Ruta al archivo de audio
            opciones: Opciones adicionales para la transcripción
            
        Returns:
            Texto transcrito
        """
        pass

class MotorTranscripcionLocal(MotorTranscripcionBase):
    """Motor de transcripción local utilizando SpeechRecognition."""
    
    def __init__(self):
        """Inicializa el motor de transcripción local."""
        self.recognizer = sr.Recognizer()
    
    def transcribir(self, ruta_archivo: str, opciones: Optional[Dict[str, Any]] = None) -> str:
        """
        Transcribe un archivo de audio a texto utilizando el reconocimiento local.
        
        Args:
            ruta_archivo: Ruta al archivo de audio
            opciones: Opciones adicionales para la transcripción
                - idioma: Código de idioma (por defecto, "es-ES")
            
        Returns:
            Texto transcrito
        """
        opciones = opciones or {}
        idioma = opciones.get("idioma", "es-ES")
        
        try:
            # Cargar el archivo de audio
            with sr.AudioFile(ruta_archivo) as fuente:
                # Ajustar el reconocedor para el ruido ambiental
                self.recognizer.adjust_for_ambient_noise(fuente)
                
                # Grabar el audio
                audio = self.recognizer.record(fuente)
                
                # Establecer tiempo de espera
                tiempo_inicio = time.time()
                
                # Utilizar el reconocedor de Google (gratuito)
                texto = self.recognizer.recognize_google(
                    audio, 
                    language=idioma,
                    show_all=False
                )
                
                # Verificar tiempo de ejecución
                tiempo_transcurrido = time.time() - tiempo_inicio
                if tiempo_transcurrido > configuracion.tiempo_espera:
                    raise ErrorTranscripcion(
                        f"La transcripción excedió el tiempo máximo de espera "
                        f"({configuracion.tiempo_espera} segundos)"
                    )
                
                return texto
                
        except sr.UnknownValueError:
            raise ErrorTranscripcion("No se pudo reconocer el audio")
        except sr.RequestError as e:
            raise ErrorTranscripcion(f"Error en la solicitud al servicio de reconocimiento: {str(e)}")
        except Exception as e:
            raise ErrorTranscripcion(f"Error durante la transcripción: {str(e)}")

class MotorTranscripcionGoogle(MotorTranscripcionBase):
    """Motor de transcripción utilizando Google Speech-to-Text API."""
    
    def __init__(self, api_clave: str):
        """
        Inicializa el motor de transcripción de Google.
        
        Args:
            api_clave: Clave de la API de Google Speech-to-Text
        """
        if not api_clave:
            raise ErrorMotorTranscripcion(
                "Se requiere una clave API para utilizar el motor de transcripción de Google"
            )
        self.api_clave = api_clave
        self.base_url = "https://speech.googleapis.com/v1/speech:recognize"
    
    def transcribir(self, ruta_archivo: str, opciones: Optional[Dict[str, Any]] = None) -> str:
        """
        Transcribe un archivo de audio a texto utilizando Google Speech-to-Text API.
        
        Args:
            ruta_archivo: Ruta al archivo de audio
            opciones: Opciones adicionales para la transcripción
                - idioma: Código de idioma (por defecto, "es-ES")
                - modelo: Modelo específico a utilizar (por defecto, "default")
            
        Returns:
            Texto transcrito
        """
        opciones = opciones or {}
        idioma = opciones.get("idioma", "es-ES")
        modelo = opciones.get("modelo", "default")
        
        try:
            # Leer el archivo de audio
            with open(ruta_archivo, "rb") as archivo_audio:
                contenido_audio = archivo_audio.read()
            
            # Codificar el contenido en base64
            import base64
            audio_codificado = base64.b64encode(contenido_audio).decode("utf-8")
            
            # Preparar la solicitud
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_clave
            }
            
            data = {
                "config": {
                    "encoding": "LINEAR16",
                    "sampleRateHertz": 16000,
                    "languageCode": idioma,
                    "model": modelo,
                    "enableAutomaticPunctuation": True
                },
                "audio": {
                    "content": audio_codificado
                }
            }
            
            # Realizar la solicitud con tiempo de espera
            tiempo_inicio = time.time()
            respuesta = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=configuracion.tiempo_espera
            )
            
            # Verificar tiempo de ejecución
            tiempo_transcurrido = time.time() - tiempo_inicio
            if tiempo_transcurrido > configuracion.tiempo_espera:
                raise ErrorTranscripcion(
                    f"La transcripción excedió el tiempo máximo de espera "
                    f"({configuracion.tiempo_espera} segundos)"
                )
            
            # Verificar la respuesta
            if respuesta.status_code != 200:
                raise ErrorTranscripcion(
                    f"Error en la API de Google Speech-to-Text: {respuesta.text}"
                )
            
            # Extraer el texto transcrito
            datos_respuesta = respuesta.json()
            
            # Verificar si hay resultados
            if not datos_respuesta.get("results"):
                return ""
            
            # Concatenar las alternativas de transcripción
            texto = ""
            for resultado in datos_respuesta["results"]:
                alternativas = resultado.get("alternatives", [])
                if alternativas:
                    texto += alternativas[0].get("transcript", "")
            
            return texto
            
        except requests.RequestException as e:
            raise ErrorTranscripcion(f"Error en la solicitud a Google Speech-to-Text: {str(e)}")
        except Exception as e:
            raise ErrorTranscripcion(f"Error durante la transcripción: {str(e)}")

# Añadir más implementaciones de motores según sea necesario
# Por ejemplo, AWS Transcribe, IBM Watson, etc.
