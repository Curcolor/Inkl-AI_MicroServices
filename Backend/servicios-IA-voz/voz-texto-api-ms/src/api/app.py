"""
Aplicación principal de la API de transcripción de voz a texto.
"""
import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from .routes import transcripcion_router, salud_router
from ..config import configuracion
from ..utils.audio_config import configurar_ffmpeg
from ..utils import ErrorBase, crear_respuesta_error

# Configurar logging
nivel_log = configuracion.nivel_log.upper()
logging.basicConfig(
    level=getattr(logging, nivel_log),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear directorio para logs si no existe
os.makedirs("logs", exist_ok=True)
# Configurar ffmpeg
configurar_ffmpeg()

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Transcripción de Voz a Texto",
    description="API para transcribir archivos de audio a texto",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejar excepciones personalizadas
@app.exception_handler(ErrorBase)
async def error_base_handler(request: Request, exc: ErrorBase):
    """Manejador para excepciones personalizadas."""
    return JSONResponse(
        status_code=500,
        content=crear_respuesta_error(
            codigo_estado=500,
            tipo_error=exc.__class__.__name__,
            mensaje=str(exc)
        )
    )

# Montar directorios estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="src/static")

# Incluir rutas
app.include_router(transcripcion_router)
app.include_router(salud_router)

# Ruta principal
@app.get("/", response_class=HTMLResponse)
async def raiz(request: Request):
    """
    Página principal con interfaz para probar la API.
    
    Args:
        request: Solicitud entrante
        
    Returns:
        Página HTML con la interfaz de prueba
    """
    return templates.TemplateResponse("index.html", {"request": request})

# Si se ejecuta directamente
if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host=configuracion.api_host, 
        port=configuracion.api_puerto, 
        reload=True
    )
