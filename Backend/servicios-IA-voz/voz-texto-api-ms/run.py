import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno primero
print("Cargando variables de entorno...")
load_dotenv()

# Importar la configuración de ffmpeg para inicializarla antes de cualquier uso de pydub
from src.utils.audio_config import configurar_ffmpeg

# Configurar ffmpeg antes de iniciar la aplicación
print("Configurando FFmpeg antes de iniciar la aplicación...")
configurar_ffmpeg()

if __name__ == "__main__":
    # Obtener configuración del servidor desde variables de entorno
    host = os.getenv("API_HOST")
    port = int(os.getenv("API_PUERTO"))
    
    # Iniciar servidor
    uvicorn.run("src.api.app:app", host=host, port=port, reload=True)
