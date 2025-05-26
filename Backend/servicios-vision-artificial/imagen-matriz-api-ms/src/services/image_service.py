"""
Servicio para la conversión de imágenes a matrices.
"""
import numpy as np
from PIL import Image
import cv2
from typing import Optional, List, BinaryIO
from io import BytesIO

class ImageService:
    @staticmethod
    async def image_to_matrix(
        image_bytes: BinaryIO,
        preprocess: Optional[List[str]] = None
    ) -> np.ndarray:
        """
        Convierte una imagen a una matriz numérica.
        
        Args:
            image_bytes: Bytes de la imagen
            preprocess: Lista de operaciones de preprocesamiento
            
        Returns:
            Matriz NumPy con los datos de la imagen
        """
        # Abrir imagen con Pillow
        img = Image.open(image_bytes)
        
        # Aplicar preprocesamiento si es necesario
        if preprocess:
            img = ImageService._apply_preprocessing(img, preprocess)
        
        # Convertir a numpy array
        matrix = np.array(img)
        return matrix
    
    @staticmethod
    def _apply_preprocessing(img: Image.Image, operations: List[str]) -> Image.Image:
        """
        Aplica operaciones de preprocesamiento a una imagen.
        
        Args:
            img: Imagen Pillow
            operations: Lista de operaciones a aplicar
            
        Returns:
            Imagen procesada
        """
        for op in operations:
            if op == "grayscale":
                img = img.convert('L')
            elif op.startswith("resize_"):
                try:
                    # Formato esperado: resize_widthxheight
                    dimensions = op.split('_')[1].split('x')
                    width, height = int(dimensions[0]), int(dimensions[1])
                    img = img.resize((width, height), Image.LANCZOS)
                except (IndexError, ValueError):
                    pass
            elif op == "normalize":
                # Convertir a numpy, normalizar y volver a Image
                img_array = np.array(img, dtype=np.float32)
                if img_array.max() > 0:
                    img_array = img_array / 255.0
                img = Image.fromarray((img_array * 255).astype(np.uint8))
        
        return img
    
    @staticmethod
    async def advanced_processing(image: np.ndarray) -> np.ndarray:
        """
        Realiza procesamiento avanzado de imágenes usando OpenCV.
        
        Args:
            image: Matriz de imagen
            
        Returns:
            Matriz procesada
        """
        # Ejemplo de procesamiento con OpenCV
        # Esta función puede expandirse según necesidades
        
        # Convertir a escala de grises si es a color
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
            
        # Detección de bordes con Canny
        edges = cv2.Canny(gray, 100, 200)
        
        return edges
