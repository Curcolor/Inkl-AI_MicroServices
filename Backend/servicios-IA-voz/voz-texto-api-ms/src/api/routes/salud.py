"""
Rutas para verificar el estado de salud de la API.
"""
from fastapi import APIRouter
from ..models import EstadoSalud
from ...config import configuracion

router = APIRouter(tags=["Salud"])

@router.get("/salud", response_model=EstadoSalud)
async def verificar_salud():
    """
    Verifica el estado de salud del servicio.
    
    Returns:
        Estado de salud del servicio
    """
    return EstadoSalud(
        estado="en línea",
        version="1.0.0",
        motor_transcripcion=configuracion.motor_transcripcion
    )
