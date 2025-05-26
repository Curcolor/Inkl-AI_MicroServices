"""
Script simple para abrir la interfaz web de MatrixToImagen
"""
import webbrowser
import time
import os
import sys

def main():
    # URL de la interfaz web
    web_ui_url = "http://localhost:8001/web"
    
    print("Abriendo la interfaz web de MatrixToImagen...")
    print(f"URL: {web_ui_url}")
    
    # Abrir la interfaz web en el navegador predeterminado
    webbrowser.open(web_ui_url)
    
    print("\nInstrucciones de uso:")
    print("1. Seleccione una imagen para cargar")
    print("2. Marque las opciones de preprocesamiento que desee aplicar")
    print("3. Haga clic en 'Verificar Transformación'")
    print("4. Espere a que se muestre la imagen de comparación")
    print("\nLa interfaz web le mostrará:")
    print("- La imagen original")
    print("- La imagen reconstruida después de la transformación")
    print("- Una visualización de la diferencia entre ambas")

if __name__ == "__main__":
    main()
