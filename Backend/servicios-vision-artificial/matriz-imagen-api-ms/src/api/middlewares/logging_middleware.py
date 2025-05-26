"""
Middleware para el registro de solicitudes y respuestas.
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.config.settings import get_settings

settings = get_settings()

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("matrix_to_image")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Registrar la solicitud entrante
        logger.info(f"Request: {request.method} {request.url}")
        
        # Procesar la solicitud
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Registrar la respuesta
            logger.info(
                f"Response: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s"
            )
            
            # Añadir el tiempo de procesamiento como header
            response.headers["X-Process-Time"] = f"{process_time:.4f}"
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url} - Error: {str(e)} - Time: {process_time:.4f}s"
            )
            raise
