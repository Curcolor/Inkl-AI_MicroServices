"""
Punto de entrada principal para la API de Texto a Voz.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import logging

from src.api.routes import router as api_router
from src.api.middlewares.logging_middleware import LoggingMiddleware
from src.config.settings import get_settings

# Obtener configuración
settings = get_settings()

# Asegurar que existe el directorio para los archivos de audio
os.makedirs(settings.AUDIO_OUTPUT_DIR, exist_ok=True)

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Texto a Voz API",
    description="API para convertir texto a voz utilizando Web Speech API en el cliente",
    version="1.0.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de logging
app.add_middleware(LoggingMiddleware)

# Montar archivos estáticos
# Referenciamos la carpeta static que está en src (fuera de api)
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Inclusión de rutas
app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para comprobar el estado de la API."""
    return JSONResponse(status_code=200, content={"status": "healthy"})

@app.get("/", tags=["Root"])
async def root():
    """
    Ruta raíz que proporciona información básica del servicio.
    """
    return {
        "servicio": "API de Texto a Voz",
        "estado": "operativo",
        "versión": "1.0.0",
        "documentación": "/docs",
        "nota": "Este servicio opera principalmente en el navegador del cliente usando Web Speech API"
    }

def main():
    """Punto de entrada para la ejecución de la API."""
    import uvicorn
    print("Servidor de texto-a-voz iniciado en modo cliente")
    print("La funcionalidad principal se ejecuta en el navegador del cliente usando Web Speech API")
    uvicorn.run("src.api.app:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.DEBUG)

if __name__ == "__main__":
    main()
