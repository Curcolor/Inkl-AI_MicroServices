import imageio_ffmpeg
from pydub import AudioSegment
import os

def configurar_ffmpeg():
    """Configura pydub para usar la versión de FFmpeg incluida con imageio-ffmpeg."""
    # Obtener la ruta al ejecutable de ffmpeg incluido en imageio-ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Configurar pydub para usar este ffmpeg
    AudioSegment.converter = ffmpeg_path
    
    # Intentar configurar ffprobe si existe
    ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe")
    if os.path.exists(ffprobe_path):
        AudioSegment.ffprobe = ffprobe_path
    
    # Añadir el directorio de ffmpeg al PATH para asegurarnos de que otros módulos lo encuentren
    ffmpeg_dir = os.path.dirname(ffmpeg_path)
    if ffmpeg_dir not in os.environ.get('PATH', ''):
        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
    
    # Imprimir información para depuración
    print(f"FFmpeg configurado en: {ffmpeg_path}")
    print(f"Directorio añadido al PATH: {ffmpeg_dir}")
    
    # Verificar la configuración
    try:
        # Intentar crear un segmento de audio vacío para verificar que ffmpeg funciona
        AudioSegment.silent(duration=1)
        print("Configuración de FFmpeg validada correctamente")
    except Exception as e:
        print(f"Error al configurar FFmpeg: {e}")
        print("Es posible que necesites instalar ffmpeg manualmente en tu sistema")
        print("O revisar si imageio-ffmpeg está correctamente instalado")