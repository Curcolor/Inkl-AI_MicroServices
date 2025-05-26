"""
Pruebas para el endpoint de salud.
"""
import pytest

def test_endpoint_salud(cliente_prueba):
    """Prueba el endpoint de salud."""
    respuesta = cliente_prueba.get("/salud")
    
    assert respuesta.status_code == 200
    datos = respuesta.json()
    
    assert "estado" in datos
    assert "version" in datos
    assert "motor_transcripcion" in datos
    
    assert datos["estado"] == "en línea"
