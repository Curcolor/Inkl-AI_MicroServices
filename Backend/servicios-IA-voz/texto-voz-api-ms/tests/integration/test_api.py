"""
Tests de integración para la API de texto a voz.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

class TestTextoVozAPI:
    """
    Clase para los tests de integración de la API de texto a voz.
    """
    
    def test_health_check(self, client):
        """Test para el endpoint de health check."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root(self, client):
        """Test para el endpoint raíz."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "servicio" in response.json()
        assert "versión" in response.json()
        assert "documentación" in response.json()
    
    def test_tts_estado(self, client):
        """Test para el endpoint de estado de TTS."""
        response = client.get("/api/tts/estado")
        
        assert response.status_code == 200
        assert response.json()["estado"] == "operativo"
        assert "mensaje" in response.json()
        assert "timestamp" in response.json()
    
    def test_tts_voces(self, client):
        """Test para el endpoint de información de voces."""
        response = client.get("/api/tts/voces")
        
        assert response.status_code == 200
        assert "mensaje" in response.json()
        assert "info" in response.json()
        assert "documentacion" in response.json()
        assert "timestamp" in response.json()
