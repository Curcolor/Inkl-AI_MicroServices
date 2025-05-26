"""
Rutas para la API de transcripción de voz a texto.
"""
import os
import tempfile
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
import json
import speech_recognition as sr
from pydub import AudioSegment

from ...services import servicio_transcripcion
from ...utils import (
    validar_archivo_audio, 
    guardar_archivo_temporal, 
    eliminar_archivo_temporal,
    normalizar_audio,
    ErrorFormatoAudio,
    ErrorTamanoArchivo,
    ErrorTranscripcion
)
from ..models import RespuestaTranscripcion, OpcionesTranscripcion

router = APIRouter(prefix="/api/v1", tags=["Transcripción"])

@router.post("/transcribir", response_model=RespuestaTranscripcion)
async def transcribir_audio(
    archivo: UploadFile = File(...),
    opciones: Optional[str] = Form(None)
):
    """
    Transcribe un archivo de audio a texto.
    
    Args:
        archivo: Archivo de audio a transcribir
        opciones: Opciones de transcripción en formato JSON (opcional)
        
    Returns:
        Texto transcrito del audio
        
    Raises:
        HTTPException: Si ocurre un error durante el proceso
    """    # Parsear opciones si se proporcionan
    opciones_dict = {}
    if opciones:
        try:
            opciones_dict = json.loads(opciones)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Las opciones proporcionadas no son un JSON válido"
            )
    
    try:  
        # Validar archivo
        validar_archivo_audio(archivo)
    
        # Variables para seguimiento de archivos
        ruta_temporal = None
        ruta_procesada = None
        archivo_convertido = False
    
        try:            # Guardar temporalmente el archivo
            ruta_temporal = guardar_archivo_temporal(archivo)
            print(f"Archivo guardado temporalmente en: {ruta_temporal}")
            
            # Verificar el formato original del archivo
            extension = os.path.splitext(ruta_temporal)[1][1:].lower()
            ruta_procesada = ruta_temporal
            
            # Forzar la conversión a WAV para asegurar compatibilidad
            print(f"Preparando archivo para transcripción. Formato original: {extension}")
            
            # Intentamos con múltiples estrategias de conversión si es necesario
            convertido_exitosamente = False
            intentos = 0
            max_intentos = 3
            
            while not convertido_exitosamente and intentos < max_intentos:
                intentos += 1
                try:
                    print(f"Intento {intentos} de {max_intentos} para convertir archivo a WAV PCM...")
                    # Liberar memoria antes de intentar la conversión
                    import gc
                    gc.collect()
                    
                    # Diferentes estrategias de conversión según el intento
                    if intentos == 1:
                        # Primer intento: conversión estándar a WAV
                        ruta_procesada, archivo_convertido = normalizar_audio(ruta_temporal, "wav")
                    elif intentos == 2:
                        # Segundo intento: forzar parámetros específicos
                        # Usamos FFmpeg directamente con parámetros específicos
                        import subprocess
                        from ...utils.audio_config import configurar_ffmpeg
                        
                        ffmpeg_path = AudioSegment.converter
                        temp_wav = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_temp.wav")
                        
                        command = [
                            ffmpeg_path, "-y", "-i", ruta_temporal,
                            "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                            temp_wav
                        ]
                        subprocess.run(command, check=True)
                        ruta_procesada = temp_wav
                        archivo_convertido = True
                    else:
                        # Tercer intento: intentar conversión con SoX si está disponible
                        try:
                            import subprocess
                            temp_wav = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_sox.wav")
                            # Verificar si sox está instalado
                            try:
                                subprocess.run(["sox", "--version"], capture_output=True, check=True)
                                # Usar SoX para la conversión
                                command = [
                                    "sox", ruta_temporal, "-r", "16000", "-b", "16", "-c", "1",
                                    temp_wav
                                ]
                                subprocess.run(command, check=True)
                                ruta_procesada = temp_wav
                                archivo_convertido = True
                            except FileNotFoundError:
                                # SoX no está instalado, usar FFmpeg con más opciones
                                ffmpeg_path = AudioSegment.converter
                                command = [
                                    ffmpeg_path, "-y", "-i", ruta_temporal, 
                                    "-f", "wav", "-bitexact", "-acodec", "pcm_s16le", 
                                    "-ar", "16000", "-ac", "1", temp_wav
                                ]
                                subprocess.run(command, check=True)
                                ruta_procesada = temp_wav
                                archivo_convertido = True
                        except Exception as e:
                            print(f"Error en tercer intento de conversión: {str(e)}")
                            # Intentaremos con el archivo original como último recurso
                            ruta_procesada = ruta_temporal
                            archivo_convertido = False
                    
                    # Verificar que el archivo resultante es válido para SpeechRecognition
                    try:
                        with sr.AudioFile(ruta_procesada) as fuente:
                            # Si no lanza excepción, el archivo es válido
                            print("Archivo convertido correctamente y validado para transcripción")
                            convertido_exitosamente = True
                    except Exception as e:
                        print(f"El archivo convertido no es válido para SpeechRecognition: {str(e)}")
                        # Intentaremos con otra estrategia en la siguiente iteración
                except Exception as e:
                    print(f"Error al convertir archivo (intento {intentos}): {str(e)}")
                    # Continuar al siguiente intento
            
            # Si no pudimos convertir exitosamente después de todos los intentos
            if not convertido_exitosamente:
                print(f"No se pudo convertir el archivo a un formato válido después de {max_intentos} intentos.")
                print("Intentando usar el archivo original como último recurso...")
                ruta_procesada = ruta_temporal
                archivo_convertido = False
            
            # Transcribir audio con el mejor archivo que tengamos
            texto = servicio_transcripcion.transcribir(ruta_procesada, opciones_dict)
            print("Transcripción completada con éxito")
            
            # Crear respuesta
            respuesta = RespuestaTranscripcion(
                texto=texto,
                # Los siguientes campos son opcionales y podrían ser
                # proporcionados por el motor de transcripción en el futuro
                confianza=None,
                idioma_detectado=opciones_dict.get("idioma"),
                duracion=None
            )
            
            return respuesta

        finally:
            # Cerrar explícitamente cualquier referencia a los archivos
            import gc
            import time
            
            # Dar tiempo a que se liberen los recursos
            print("Esperando a que se liberen los recursos antes de limpiar...")
            time.sleep(1)  # Esperar 1 segundo
            gc.collect()  # Forzar la recolección de basura
            
            # SOLO eliminar el archivo convertido temporal, no el original
            # El archivo original se mantendrá para evitar problemas de acceso
            if archivo_convertido and ruta_procesada and ruta_procesada != ruta_temporal:
                print(f"Limpiando archivo convertido: {ruta_procesada}")
                eliminar_archivo_temporal(ruta_procesada)
            
            # Ya no eliminamos el archivo original para evitar errores
            # Los archivos temporales se eliminarán automáticamente por el sistema
            if ruta_temporal:
                print(f"El archivo original {ruta_temporal} se mantendrá para evitar errores de acceso")
    
    except ErrorFormatoAudio as e:
        raise HTTPException(status_code=415, detail=str(e))
    except ErrorTamanoArchivo as e:
        raise HTTPException(status_code=413, detail=str(e))
    except ErrorTranscripcion as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
