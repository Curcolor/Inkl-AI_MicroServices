"""
Punto de entrada principal para la API ImageToMatrix.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import router as api_router
from src.api.middlewares.logging_middleware import LoggingMiddleware
from src.config.settings import get_settings

settings = get_settings()

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="ImageToMatrix API",
    description="API para convertir imágenes a matrices numéricas",
    version="0.1.0",
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

# Inclusión de rutas
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para comprobar el estado de la API."""
    return JSONResponse(status_code=200, content={"status": "healthy"})

def main():
    """Punto de entrada para la ejecución de la API."""
    import uvicorn
    uvicorn.run("src.api.app:app", host=settings.API_HOST, port=settings.API_PORT, reload=settings.DEBUG)

if __name__ == "__main__":
    main()
