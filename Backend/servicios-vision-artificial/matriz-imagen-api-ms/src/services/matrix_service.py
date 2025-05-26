"""
Servicio para la conversión de matrices a imágenes.
"""
import numpy as np
from PIL import Image
import cv2
import io
import json
import base64
from typing import Dict, List, Union, BinaryIO, Tuple
import matplotlib.pyplot as plt

class MatrixService:
    @staticmethod
    async def matrix_to_image(
        matrix_data: Union[Dict, BinaryIO, str],
        format: str,
        output_format: str = "png"
    ) -> Tuple[bytes, str]:
        """
        Convierte una matriz numérica a una imagen.
        
        Args:
            matrix_data: Datos de la matriz en formato JSON o NumPy serializado
            format: Formato de entrada ('json' o 'numpy')
            output_format: Formato de salida de la imagen
            
        Returns:
            Tupla con los bytes de la imagen y el tipo de contenido
        """
        # Convertir los datos de entrada a una matriz NumPy
        matrix = MatrixService._parse_matrix_input(matrix_data, format)
        
        # Realizar la conversión a imagen
        img_bytes = MatrixService._convert_matrix_to_image_bytes(matrix, output_format)
        
        # Definir el tipo MIME según el formato de salida
        content_type = f"image/{output_format}"
        
        return img_bytes, content_type
    
    @staticmethod
    def _parse_matrix_input(
        data: Union[Dict, BinaryIO, str],
        format: str
    ) -> np.ndarray:
        """
        Parsea los datos de entrada en una matriz NumPy.
        
        Args:
            data: Datos de entrada en formato JSON o NumPy serializado
            format: Formato de los datos ('json' o 'numpy')
            
        Returns:
            Matriz NumPy
        """
        if format.lower() == "json":
            # Si es un diccionario, extraer directamente
            if isinstance(data, dict):
                matrix_data = data.get("matrix")
                if not matrix_data:
                    raise ValueError("El formato JSON no contiene la clave 'matrix'")
                return np.array(matrix_data)
            
            # Si es una cadena JSON
            if isinstance(data, str):
                try:
                    json_data = json.loads(data)
                    matrix_data = json_data.get("matrix")
                    if not matrix_data:
                        raise ValueError("El formato JSON no contiene la clave 'matrix'")
                    return np.array(matrix_data)
                except json.JSONDecodeError:
                    raise ValueError("Error al decodificar JSON")
            
            # Si son bytes JSON
            try:
                json_data = json.loads(data)
                matrix_data = json_data.get("matrix")
                if not matrix_data:
                    raise ValueError("El formato JSON no contiene la clave 'matrix'")
                return np.array(matrix_data)
            except (json.JSONDecodeError, TypeError, AttributeError):
                raise ValueError("Formato de datos JSON no válido")
        
        elif format.lower() == "numpy":
            try:
                # Si es un archivo binario o bytes directos
                if hasattr(data, 'read'):
                    return np.load(data)
                elif isinstance(data, bytes):
                    buffer = io.BytesIO(data)
                    return np.load(buffer)
                else:
                    raise ValueError("Formato de datos NumPy no válido")
            except Exception as e:
                raise ValueError(f"Error al cargar matriz NumPy: {str(e)}")
        
        else:
            raise ValueError(f"Formato no admitido: {format}")
    
    @staticmethod
    def _convert_matrix_to_image_bytes(matrix: np.ndarray, output_format: str) -> bytes:
        """
        Convierte una matriz NumPy en bytes de imagen.
        
        Args:
            matrix: Matriz NumPy con los datos de la imagen
            output_format: Formato de salida de la imagen
            
        Returns:
            Bytes de la imagen
        """
        # Verificar dimensiones
        if len(matrix.shape) not in [2, 3]:
            raise ValueError("La matriz debe ser 2D (escala grises) o 3D (color)")
        
        # Normalización si los valores están entre 0 y 1
        if matrix.dtype == np.float32 or matrix.dtype == np.float64:
            if np.max(matrix) <= 1.0:
                matrix = (matrix * 255).astype(np.uint8)
        
        # Convertir a uint8 si es necesario
        if matrix.dtype != np.uint8:
            matrix = matrix.astype(np.uint8)
        
        # Crear imagen desde matriz
        if len(matrix.shape) == 2:  # Escala de grises
            img = Image.fromarray(matrix, mode='L')
        elif matrix.shape[2] == 1:  # Escala de grises con dimensión adicional
            img = Image.fromarray(matrix.squeeze(), mode='L')
        elif matrix.shape[2] == 3:  # RGB
            img = Image.fromarray(matrix, mode='RGB')
        elif matrix.shape[2] == 4:  # RGBA
            img = Image.fromarray(matrix, mode='RGBA')
        else:
            raise ValueError(f"Dimensiones de matriz no compatibles: {matrix.shape}")
        
        # Convertir a bytes en el formato solicitado
        img_buffer = io.BytesIO()
        img.save(img_buffer, format=output_format.upper())
        img_buffer.seek(0)
        
        return img_buffer.getvalue()
    
    @staticmethod
    async def generate_comparison_image(
        original_image_bytes: bytes,
        reconstructed_image_bytes: bytes
    ) -> bytes:
        """
        Genera una imagen de comparación entre la original y la reconstruida.
        
        Args:
            original_image_bytes: Bytes de la imagen original
            reconstructed_image_bytes: Bytes de la imagen reconstruida
            
        Returns:
            Bytes de la imagen de comparación
        """
        # Cargar imágenes
        original_img = Image.open(io.BytesIO(original_image_bytes))
        reconstructed_img = Image.open(io.BytesIO(reconstructed_image_bytes))
        
        # Convertir a RGB si es necesario
        if original_img.mode != 'RGB':
            original_img = original_img.convert('RGB')
        if reconstructed_img.mode != 'RGB':
            reconstructed_img = reconstructed_img.convert('RGB')
        
        # Asegurar que ambas imágenes tengan el mismo tamaño
        width = max(original_img.width, reconstructed_img.width)
        height = max(original_img.height, reconstructed_img.height)
        
        if original_img.size != (width, height):
            original_img = original_img.resize((width, height), Image.LANCZOS)
        if reconstructed_img.size != (width, height):
            reconstructed_img = reconstructed_img.resize((width, height), Image.LANCZOS)
        
        # Convertir a arrays NumPy
        original_array = np.array(original_img)
        reconstructed_array = np.array(reconstructed_img)
        
        # Calcular diferencia absoluta
        diff_array = np.abs(original_array.astype(np.float32) - reconstructed_array.astype(np.float32)).astype(np.uint8)
        
        # Crear imagen de diferencia
        diff_img = Image.fromarray(diff_array)
        
        # Crear figura de comparación
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Mostrar imágenes
        axes[0].imshow(np.array(original_img))
        axes[0].set_title("Imagen Original")
        axes[0].axis("off")
        
        axes[1].imshow(np.array(reconstructed_img))
        axes[1].set_title("Imagen Reconstruida")
        axes[1].axis("off")
        
        axes[2].imshow(np.array(diff_img))
        axes[2].set_title("Diferencia")
        axes[2].axis("off")
        
        # Guardar a bytes
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        
        return buf.getvalue()
