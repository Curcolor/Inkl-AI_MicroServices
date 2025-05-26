"""
Utilidades para el procesamiento avanzado de imágenes.
"""
import numpy as np
import cv2
from typing import Tuple, Optional, Dict, Any

class ImageProcessingUtils:
    @staticmethod
    def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """
        Redimensiona una imagen al tamaño especificado.
        
        Args:
            image: Matriz de la imagen
            target_size: (ancho, alto) objetivo
            
        Returns:
            Imagen redimensionada como matriz numpy
        """
        return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
    
    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """
        Normaliza los valores de píxeles al rango [0, 1].
        
        Args:
            image: Matriz de la imagen
            
        Returns:
            Imagen normalizada como matriz numpy
        """
        if image.dtype != np.float32 and image.dtype != np.float64:
            image = image.astype(np.float32)
            
        if np.max(image) > 0:
            image = image / 255.0
            
        return image
    
    @staticmethod
    def extract_image_features(
        image: np.ndarray, 
        feature_type: str = "hog"
    ) -> Dict[str, Any]:
        """
        Extrae características de una imagen para su análisis.
        
        Args:
            image: Matriz de la imagen
            feature_type: Tipo de características a extraer (hog, sift, orb)
            
        Returns:
            Diccionario con las características extraídas
        """
        result = {}
        
        # Asegurar que la imagen está en escala de grises para algunos extractores
        if len(image.shape) > 2 and image.shape[2] > 1:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        if feature_type == "hog":
            # Histograma de Gradientes Orientados
            # Parámetros para HOG
            win_size = (64, 64)
            block_size = (16, 16)
            block_stride = (8, 8)
            cell_size = (8, 8)
            nbins = 9
            
            # Redimensionar para HOG si es necesario
            if gray.shape[0] < 64 or gray.shape[1] < 64:
                gray = cv2.resize(gray, (64, 64))
                
            hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
            features = hog.compute(gray)
            result["hog_features"] = features
            result["feature_size"] = features.shape
            
        elif feature_type == "sift":
            # SIFT (Scale-Invariant Feature Transform)
            sift = cv2.SIFT_create()
            keypoints, descriptors = sift.detectAndCompute(gray, None)
            result["keypoints_count"] = len(keypoints)
            result["feature_size"] = descriptors.shape if descriptors is not None else None
            # No podemos devolver keypoints directamente en JSON, pero podemos extraer coordenadas
            if keypoints:
                result["keypoint_locations"] = [(kp.pt[0], kp.pt[1]) for kp in keypoints[:10]]  # Primeros 10 keypoints
            
        elif feature_type == "orb":
            # ORB (Oriented FAST and Rotated BRIEF)
            orb = cv2.ORB_create()
            keypoints, descriptors = orb.detectAndCompute(gray, None)
            result["keypoints_count"] = len(keypoints)
            result["feature_size"] = descriptors.shape if descriptors is not None else None
            if keypoints:
                result["keypoint_locations"] = [(kp.pt[0], kp.pt[1]) for kp in keypoints[:10]]
                
        return result
