"""
Script para probar la configuración de la aplicación.
"""
import sys
print(f"Python version: {sys.version}")

try:
    from src.config.settings import get_settings
    settings = get_settings()
    print("Configuración cargada correctamente:")
    print(f"API_HOST: {settings.API_HOST}")
    print(f"API_PORT: {settings.API_PORT}")
    print("La configuración funciona correctamente!")
except Exception as e:
    print(f"Error al cargar la configuración: {str(e)}")
    import traceback
    traceback.print_exc()
