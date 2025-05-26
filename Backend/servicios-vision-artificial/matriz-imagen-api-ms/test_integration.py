"""
Script de prueba para verificar el funcionamiento de MatrixToImagen
"""
import requests
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import base64
import time
import sys
import os

def main():
    # URL de los servicios
    imagetomatrix_url = "http://localhost:8000/api/v1/convert"
    matrixtoimagen_url = "http://localhost:8001/api/v1/verify"
    api_key = "development_key_change_me"
    
    # 1. Crear una imagen de prueba
    print("Creando imagen de prueba...")
    img = Image.new('RGB', (300, 200), color='white')
    
    # Dibujar algunos elementos
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Círculo rojo
    draw.ellipse((50, 50, 150, 150), fill='red')
    
    # Rectángulo azul
    draw.rectangle((200, 50, 250, 150), fill='blue')
    
    # Línea verde
    draw.line((20, 180, 280, 180), fill='green', width=5)
    
    # Guardar la imagen temporalmente
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_image.png")
    img.save(img_path)
    print(f"Imagen guardada en: {img_path}")
    
    # 2. Verificar si los servicios están activos
    try:
        health_response = requests.get("http://localhost:8001/health")
        if health_response.status_code != 200:
            print(f"Error: MatrixToImagen no está respondiendo. Status: {health_response.status_code}")
            return
        
        print("MatrixToImagen está activo")
        
        health_response = requests.get("http://localhost:8000/health")
        if health_response.status_code != 200:
            print(f"Error: ImageToMatrix no está respondiendo. Status: {health_response.status_code}")
            return
            
        print("ImageToMatrix está activo")
    except Exception as e:
        print(f"Error al verificar servicios: {str(e)}")
        return
    
    # 3. Verificar transformación directamente usando el endpoint /verify
    print("\nVerificando transformación imagen-matriz-imagen...")
    
    try:
        with open(img_path, "rb") as img_file:
            files = {"image": ("test_image.png", img_file, "image/png")}
            headers = {"X-API-Key": api_key}
            
            # Con preprocesamiento de escala de grises
            response = requests.post(
                matrixtoimagen_url,
                files=files,
                headers=headers,
                data={"preprocess": "grayscale"}
            )
            
            if response.status_code != 200:
                print(f"Error en la verificación: {response.status_code}")
                print(response.text)
                return
            
            # Guardar la imagen de comparación
            comparison_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparison_grayscale.png")
            with open(comparison_path, "wb") as f:
                f.write(response.content)
            print(f"Comparación con escala de grises guardada en: {comparison_path}")
            
        # Otra prueba: con normalización
        with open(img_path, "rb") as img_file:
            files = {"image": ("test_image.png", img_file, "image/png")}
            headers = {"X-API-Key": api_key}
            
            # Con preprocesamiento de normalización
            response = requests.post(
                matrixtoimagen_url,
                files=files,
                headers=headers,
                data={"preprocess": "normalize"}
            )
            
            if response.status_code != 200:
                print(f"Error en la verificación: {response.status_code}")
                print(response.text)
                return
            
            # Guardar la imagen de comparación
            comparison_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparison_normalize.png")
            with open(comparison_path, "wb") as f:
                f.write(response.content)
            print(f"Comparación con normalización guardada en: {comparison_path}")
            
        print("\nPrueba completada con éxito.")
        print("Puedes abrir las imágenes generadas para verificar visualmente el resultado.")
        
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")

if __name__ == "__main__":
    main()
