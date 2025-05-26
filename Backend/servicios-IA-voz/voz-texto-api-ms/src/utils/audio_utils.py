"""
Módulo de utilidades para el procesamiento de archivos de audio.
"""
import os
import tempfile
import uuid
from typing import Optional, Tuple
from pydub import AudioSegment
from fastapi import UploadFile
import speech_recognition as sr

from ..config import configuracion
from .error_utils import ErrorFormatoAudio, ErrorTamanoArchivo

def obtener_extension(archivo: UploadFile) -> str:
    """
    Obtiene la extensión del archivo.
    
    Args:
        archivo: Archivo de audio
        
    Returns:
        Extensión del archivo
    """
    # Diccionario de mapeo de tipos MIME a extensiones
    mime_to_ext = {
        'audio/webm': 'webm',
        'video/webm': 'webm',
        'audio/mpeg': 'mp3',
        'audio/mp3': 'mp3',
        'audio/wav': 'wav',
        'audio/wave': 'wav',
        'audio/x-wav': 'wav',
        'audio/vnd.wave': 'wav',
        'audio/ogg': 'ogg',
        'audio/opus': 'ogg',
        'audio/vorbis': 'ogg',
        'audio/flac': 'flac',
        'audio/x-flac': 'flac',
        'audio/x-aiff': 'aiff',
        'audio/aiff': 'aiff',
        'audio/x-m4a': 'm4a',
        'audio/mp4': 'm4a',
        'audio/aac': 'aac'
    }
    
    # Obtener el tipo de contenido
    content_type = archivo.content_type if hasattr(archivo, 'content_type') else None
    content_type_ext = None
    
    # Si tenemos un tipo de contenido, intentar mapear a una extensión
    if content_type:
        # Eliminar parámetros adicionales como ';codecs=...'
        base_content_type = content_type.split(';')[0].strip().lower()
        content_type_ext = mime_to_ext.get(base_content_type)
        
        if content_type_ext:
            print(f"Extensión detectada desde tipo MIME {base_content_type}: {content_type_ext}")
    
    # Si no hay nombre de archivo, usar la extensión del tipo de contenido
    if not archivo.filename:
        return content_type_ext or ""
    
    # Comprobar si hay un punto en el nombre del archivo
    if '.' not in archivo.filename:
        return content_type_ext or ""
    
    # Obtener la extensión del nombre del archivo
    extension_filename = archivo.filename.split(".")[-1].lower()
    
    # Si tenemos tanto extensión del nombre como del tipo MIME y son diferentes,
    # verificar cuál usar
    if content_type_ext and extension_filename != content_type_ext:
        print(f"La extensión del archivo ({extension_filename}) no coincide con el tipo de contenido "
              f"({content_type}, ext={content_type_ext})")
        
        # Verificar si la extensión del filename está en nuestro diccionario de MIME,
        # si no lo está, preferimos la del tipo MIME
        if any(extension_filename == ext for ext in mime_to_ext.values()):
            print(f"Usando extensión del nombre de archivo: {extension_filename}")
            return extension_filename
        else:
            print(f"Usando extensión del tipo MIME: {content_type_ext}")
            return content_type_ext
    
    return extension_filename

def validar_archivo_audio(archivo: UploadFile) -> None:
    """
    Valida que el archivo sea un archivo de audio válido.
    
    Args:
        archivo: Archivo de audio a validar
        
    Raises:
        ErrorFormatoAudio: Si el formato del archivo no es soportado
        ErrorTamanoArchivo: Si el archivo excede el tamaño máximo permitido
    """
    # Información de depuración
    print(f"Validando archivo de audio: {archivo.filename}")
    print(f"Tipo de contenido: {archivo.content_type if hasattr(archivo, 'content_type') else 'No disponible'}")
    
    # Verificar el tamaño del archivo
    if hasattr(archivo, "size"):
        tamano_mb = archivo.size / (1024 * 1024)  # Convertir a MB
    else:
        # Si no se puede obtener el tamaño directamente, leer el archivo en memoria
        contenido = archivo.file.read()
        # Volver a la posición inicial del archivo
        archivo.file.seek(0)
        tamano_mb = len(contenido) / (1024 * 1024)  # Convertir a MB
    
    if tamano_mb > configuracion.tamano_max_archivo:
        raise ErrorTamanoArchivo(
            f"El archivo excede el tamaño máximo permitido de "
            f"{configuracion.tamano_max_archivo} MB. "
            f"Tamaño actual: {tamano_mb:.2f} MB"
        )
    
    # Obtener la extensión del archivo
    extension = obtener_extension(archivo)
    
    # Si no se pudo determinar la extensión, intentar obtenerla del tipo de contenido
    if not extension and hasattr(archivo, 'content_type'):
        content_type = archivo.content_type
        if 'audio/' in content_type or 'video/' in content_type:  # webm puede ser video/webm para audio
            # Extraer la extensión del tipo de contenido
            extension = content_type.split('/')[-1].split(';')[0]
            print(f"Determinando extensión desde content_type: {extension}")
    
    # Lista de formatos permitidos desde la configuración
    formatos_permitidos = [
        formato.strip().lower() for formato in 
        configuracion.formatos_permitidos.split(',')
    ]
    
    # Añadir algunos formatos comunes que siempre deberían ser permitidos
    formatos_siempre_permitidos = ['wav', 'webm', 'mp3', 'ogg', 'flac', 'aiff', 'aif', 'm4a']
    for formato in formatos_siempre_permitidos:
        if formato not in formatos_permitidos:
            formatos_permitidos.append(formato)

    print(f"Formatos permitidos: {formatos_permitidos}")
    print(f"Extensión detectada: {extension}")
    
    # Verificar si la extensión está en la lista de formatos permitidos
    if extension and extension.lower() in formatos_permitidos:
        return
    
    # Si hemos llegado hasta aquí, el formato no es válido
    raise ErrorFormatoAudio(
        f"Formato de audio no soportado: {extension or 'desconocido'}. "
        f"Los formatos permitidos son: {', '.join(formatos_permitidos)}"
    )

def guardar_archivo_temporal(archivo: UploadFile) -> str:
    """
    Guarda el archivo en una ubicación temporal.
    
    Args:
        archivo: Archivo de audio a guardar
        
    Returns:
        Ruta al archivo temporal
    """
    # Crear un archivo temporal con un nombre único
    nombre_temp = f"{uuid.uuid4()}.{obtener_extension(archivo)}"
    ruta_temp = os.path.join(tempfile.gettempdir(), nombre_temp)
    
    # Guardar el contenido del archivo en el archivo temporal
    with open(ruta_temp, "wb") as f:
        # Leer el archivo en chunks para evitar problemas de memoria
        for chunk in iter(lambda: archivo.file.read(1024 * 1024), b""):
            f.write(chunk)
    
    return ruta_temp

def eliminar_archivo_temporal(ruta_archivo: str) -> None:
    """
    Elimina un archivo temporal.
    
    Args:
        ruta_archivo: Ruta al archivo a eliminar
    """
    import time
    
    if not os.path.exists(ruta_archivo):
        return
    
    # Intentar eliminar el archivo con reintentos
    max_intentos = 3
    intentos = 0
    while intentos < max_intentos:
        try:
            os.close(os.open(ruta_archivo, os.O_RDONLY))  # Cerrar cualquier descriptor abierto
            os.remove(ruta_archivo)
            print(f"Archivo temporal eliminado: {ruta_archivo}")
            break
        except PermissionError:
            # Si falla por PermissionError, esperar e intentar de nuevo
            print(f"No se pudo eliminar el archivo {ruta_archivo}. Reintentando...")
            intentos += 1
            time.sleep(1)  # Esperar 1 segundo antes de reintentar
        except Exception as e:
            # Para otros errores, registrar y continuar
            print(f"Error al eliminar archivo temporal {ruta_archivo}: {str(e)}")
            break

def normalizar_audio(ruta_archivo: str, formato_salida: Optional[str] = None) -> Tuple[str, bool]:
    """
    Normaliza un archivo de audio y lo convierte a un formato específico si es necesario.
    
    Args:
        ruta_archivo: Ruta al archivo de audio
        formato_salida: Formato de salida (por defecto, el mismo que el de entrada)
        
    Returns:
        Tupla con la ruta al archivo normalizado y un booleano que indica si se creó un nuevo archivo
    """
    # Obtener la extensión del archivo original
    extension_original = os.path.splitext(ruta_archivo)[1][1:].lower()
    
    # Si no se especifica un formato de salida, usar el mismo que el original
    if not formato_salida:
        formato_salida = extension_original
    
    # Si el formato de entrada y salida son iguales pero es WAV,
    # verificamos que sea PCM WAV
    if formato_salida == extension_original and extension_original == "wav":
        print("Verificando si el archivo WAV es compatible con PCM")
        try:
            # Intentar cargar el archivo para verificar si es compatible
            sr.AudioFile(ruta_archivo)
            print("El archivo WAV ya es compatible con PCM")
            return ruta_archivo, False
        except Exception as e:
            print(f"El archivo WAV no es compatible con PCM, se realizará conversión: {str(e)}")
            # Continuar con la conversión
    elif formato_salida == extension_original:
        # Para otros formatos, si son iguales, no hacemos conversión
        return ruta_archivo, False
    
    # Información de depuración
    print(f"Convirtiendo archivo desde '{extension_original}' a '{formato_salida}'")
    
    # Crear un nuevo nombre de archivo para el archivo convertido
    nombre_base = os.path.basename(ruta_archivo)
    nombre_sin_extension = os.path.splitext(nombre_base)[0]
    nuevo_nombre = f"{nombre_sin_extension}_convertido.{formato_salida}"
    nueva_ruta = os.path.join(tempfile.gettempdir(), nuevo_nombre)
    
    # Intentar diferentes métodos de conversión
    try:
        # Método 1: Usar pydub para convertir a PCM WAV
        try:
            print("Intentando conversión a PCM WAV con pydub...")
            audio = AudioSegment.from_file(ruta_archivo, format=extension_original)
            
            # Asegurarnos de que sea PCM WAV (16 bits, 44100 Hz)
            if audio.sample_width != 2 or audio.frame_rate != 44100:
                print(f"Normalizando audio: {audio.sample_width} bits, {audio.frame_rate} Hz")
                # Convertir a 16 bits y 44100 Hz
                audio = audio.set_sample_width(2)
                audio = audio.set_frame_rate(44100)
            
            # Exportar como PCM WAV
            if formato_salida.lower() == "wav":
                audio.export(nueva_ruta, format="wav", parameters=["-acodec", "pcm_s16le"])
            else:
                audio.export(nueva_ruta, format=formato_salida)
                
            print("Conversión con pydub exitosa")
            return nueva_ruta, True
        except Exception as e:
            print(f"Error al convertir con pydub: {str(e)}")
            
            # Método 2: Usar ffmpeg directamente con parámetros específicos para PCM WAV
            try:
                import subprocess
                print("Intentando conversión directa con ffmpeg a PCM WAV...")
                ffmpeg_path = AudioSegment.converter
                
                if formato_salida.lower() == "wav":
                    # Parámetros específicos para PCM WAV
                    command = [
                        ffmpeg_path, "-y", "-i", ruta_archivo,
                        "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1",
                        nueva_ruta
                    ]
                else:
                    command = [ffmpeg_path, "-y", "-i", ruta_archivo, nueva_ruta]
                
                subprocess.run(command, check=True, capture_output=True)
                print("Conversión directa con ffmpeg exitosa")
                
                # Verificar que el archivo resultante es compatible
                try:
                    sr.AudioFile(nueva_ruta)
                    print("Se ha verificado que el archivo convertido es compatible")
                except Exception as e:
                    print(f"ADVERTENCIA: El archivo convertido puede no ser compatible: {str(e)}")
                
                return nueva_ruta, True
            except Exception as e:
                print(f"Error al convertir directamente con ffmpeg: {str(e)}")
                
                # Método 3: Último intento - usar ffmpeg con más opciones
                try:
                    import subprocess
                    print("Último intento de conversión con ffmpeg...")
                    # Usar opciones más específicas para asegurar compatibilidad
                    temp_wav = os.path.join(tempfile.gettempdir(), f"{nombre_sin_extension}_temp.wav")
                    command = [
                        ffmpeg_path, "-y", "-i", ruta_archivo,
                        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", 
                        "-f", "wav", temp_wav
                    ]
                    subprocess.run(command, check=True, capture_output=True)
                    print("Conversión a WAV temporal exitosa")
                    
                    # Ahora convertimos al formato final
                    command = [ffmpeg_path, "-y", "-i", temp_wav, nueva_ruta]
                    subprocess.run(command, check=True, capture_output=True)
                    print("Conversión final exitosa")
                    
                    # Limpiar archivo temporal
                    if os.path.exists(temp_wav):
                        os.remove(temp_wav)
                    
                    return nueva_ruta, True
                except Exception as e:
                    print(f"Error en último intento de conversión: {str(e)}")
                    # Si todos los métodos fallan, lanzar excepción
                    raise ErrorFormatoAudio(f"No se pudo convertir el archivo a un formato compatible. Error: {str(e)}")
    finally:
        # Liberar recursos
        import gc
        gc.collect()  # Forzar la recolección de basura

def segmentar_audio(ruta_archivo: str, duracion_segmento: int = 60000) -> list[str]:
    """
    Segmenta un archivo de audio largo en segmentos más pequeños.
    
    Args:
        ruta_archivo: Ruta al archivo de audio
        duracion_segmento: Duración de cada segmento en milisegundos (por defecto 60s)
        
    Returns:
        Lista de rutas a los segmentos de audio
    """
    # Obtener la extensión del archivo
    extension = os.path.splitext(ruta_archivo)[1][1:].lower()
    
    # Cargar el archivo de audio con pydub
    try:
        audio = AudioSegment.from_file(ruta_archivo, format=extension)
    except Exception as e:
        raise ErrorFormatoAudio(f"Error al procesar el archivo de audio: {str(e)}")
    
    # Si el audio es más corto que la duración del segmento, devolver solo la ruta original
    if len(audio) <= duracion_segmento:
        return [ruta_archivo]
    
    # Segmentar el audio
    segmentos = []
    for i in range(0, len(audio), duracion_segmento):
        # Extraer el segmento
        segmento = audio[i:i + duracion_segmento]
        
        # Crear un nombre único para el segmento
        nombre_base = os.path.basename(ruta_archivo)
        nombre_sin_extension = os.path.splitext(nombre_base)[0]
        nombre_segmento = f"{nombre_sin_extension}_segmento_{i // duracion_segmento}.{extension}"
        ruta_segmento = os.path.join(tempfile.gettempdir(), nombre_segmento)
        
        # Exportar el segmento
        segmento.export(ruta_segmento, format=extension)
        
        # Añadir la ruta del segmento a la lista
        segmentos.append(ruta_segmento)
    
    return segmentos
