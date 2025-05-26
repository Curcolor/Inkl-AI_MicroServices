"""
Middleware para el registro y las métricas de la API.
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar solicitudes y respuestas HTTP.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        """
        Procesa una solicitud HTTP y registra información relevante.
        
        Args:
            request: La solicitud HTTP entrante
            call_next: La función para llamar al siguiente middleware
            
        Returns:
            La respuesta HTTP
        """
        start_time = time.time()
        
        # Registrar la solicitud entrante
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Procesar la solicitud
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Registrar la respuesta con el tiempo de procesamiento
            logger.info(
                f"Response: {request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Processed in: {process_time:.4f}s"
            )
            
            # Añadir cabecera con el tiempo de procesamiento
            response.headers["X-Process-Time"] = f"{process_time:.4f}"
            
            return response
        except Exception as e:
            # Registrar errores
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url.path} - "
                f"Error: {str(e)} - "
                f"Processed in: {process_time:.4f}s"
            )
            raise
