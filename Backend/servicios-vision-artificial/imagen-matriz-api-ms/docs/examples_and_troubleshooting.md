# Ejemplos y Solución de Problemas - ImageToMatrix API

## Ejemplos de uso de la API

### Ejemplos en Python

```python
import requests
import numpy as np
import json
import io

# URL base de la API
BASE_URL = "http://localhost:8000"
API_KEY = "development_key_change_me"

# Función para convertir una imagen a matriz
def image_to_matrix(image_path, preprocess=None, format="json"):
    """
    Convierte una imagen en una matriz usando la API ImageToMatrix.
    
    Args:
        image_path: Ruta al archivo de imagen
        preprocess: Lista de operaciones de preprocesamiento (opcional)
        format: Formato de salida ('json' o 'numpy')
        
    Returns:
        Matriz numpy con los datos de la imagen procesada
    """
    url = f"{BASE_URL}/api/v1/convert"
    
    # Preparar cabeceras
    headers = {
        "X-API-Key": API_KEY
    }
    
    # Preparar archivos y datos
    files = {
        "image": open(image_path, "rb")
    }
    
    data = {
        "format": format
    }
    
    # Añadir preprocesamiento si se especifica
    if preprocess:
        if isinstance(preprocess, list):
            preprocess = ",".join(preprocess)
        data["preprocess"] = preprocess
    
    # Hacer la solicitud
    response = requests.post(url, headers=headers, files=files, data=data)
    
    # Comprobar si la solicitud fue exitosa
    response.raise_for_status()
    
    # Procesar la respuesta según el formato solicitado
    if format == "json":
        result = response.json()
        # Convertir la lista a matriz numpy
        matrix = np.array(result["matrix"], dtype=result["dtype"])
        return matrix
    elif format == "numpy":
        # Cargar directamente la matriz desde los bytes devueltos
        return np.load(io.BytesIO(response.content))

# Ejemplo 1: Conversión simple a formato JSON
matrix = image_to_matrix("ruta/a/imagen.jpg")
print(f"Forma de la matriz: {matrix.shape}")

# Ejemplo 2: Aplicar preprocesamiento
matrix_gray = image_to_matrix(
    "ruta/a/imagen.jpg",
    preprocess=["grayscale", "normalize"]
)
print(f"Forma de la matriz en escala de grises: {matrix_gray.shape}")
print(f"Valores normalizados: min={matrix_gray.min()}, max={matrix_gray.max()}")

# Ejemplo 3: Redimensionar a un tamaño específico
matrix_resized = image_to_matrix(
    "ruta/a/imagen.jpg",
    preprocess=["resize_224x224"]
)
print(f"Forma de la matriz redimensionada: {matrix_resized.shape}")
```

### Ejemplos con cURL

#### Conversión simple

```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -F "image=@ruta/a/imagen.jpg"
```

#### Con preprocesamiento

```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -F "image=@ruta/a/imagen.jpg" \
  -F "preprocess=grayscale,normalize,resize_224x224"
```

#### Guardando la salida en formato JSON

```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -F "image=@ruta/a/imagen.jpg" \
  -o resultado.json
```

#### Formato NumPy

```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -F "image=@ruta/a/imagen.jpg" \
  -F "format=numpy" \
  -o matriz.npy
```

### Ejemplos con Postman

1. Crea una nueva solicitud POST a `http://localhost:8000/api/v1/convert`

2. En la pestaña "Headers", añade:
   - Key: `X-API-Key`
   - Value: `development_key_change_me`

3. En la pestaña "Body":
   - Selecciona "form-data"
   - Añade una clave `image` de tipo File y selecciona tu imagen
   - Añade una clave `preprocess` de tipo Text con valor `grayscale,normalize` (opcional)
   - Añade una clave `format` de tipo Text con valor `json` (opcional)

4. Envía la solicitud y verás la respuesta con la matriz

## Casos de uso comunes

### 1. Preprocesamiento para entrenamiento de redes neuronales

```python
import requests
import numpy as np
from PIL import Image
import io

def get_training_batch(image_paths, target_size=(224, 224)):
    """Prepara un lote de imágenes para entrenamiento de redes neuronales."""
    batch = []
    
    for path in image_paths:
        # Usar la API para preprocesar la imagen
        preprocessed = image_to_matrix(
            path,
            preprocess=[
                "grayscale",
                "normalize",
                f"resize_{target_size[0]}x{target_size[1]}"
            ]
        )
        batch.append(preprocessed)
    
    # Convertir a array de numpy con forma [batch_size, height, width, channels]
    return np.array(batch)
```

### 2. Extracción de características para clasificación

```python
def extract_features_from_image(image_path):
    """Extrae características para clasificación de imágenes."""
    # Primero convertimos a matriz
    matrix = image_to_matrix(image_path, preprocess=["grayscale"])
    
    # Aplicamos HOG u otro extractor de características
    # (Esto podría ser una extensión futura de la API)
    features = compute_hog_features(matrix)
    
    return features
```

### 3. Procesamiento por lotes

```bash
#!/bin/bash

# Procesar todas las imágenes en un directorio
for img in ./imagenes/*.jpg; do
    echo "Procesando $img..."
    curl -s -X POST \
      http://localhost:8000/api/v1/convert \
      -H "X-API-Key: development_key_change_me" \
      -F "image=@$img" \
      -F "preprocess=grayscale,normalize" \
      -o "${img%.jpg}.json"
done
```

### 4. Extracción de características avanzadas

La API incluye funcionalidades avanzadas para extraer características de imágenes que son útiles para tareas de visión por computadora. Aunque estas funcionalidades no están directamente expuestas como endpoints, pueden ser implementadas fácilmente extendiendo la API.

#### Ejemplo de implementación de un extractor HOG

```python
import requests
import numpy as np
import cv2
import io

def extract_hog_features(image_path):
    """Extrae características HOG de una imagen usando la API."""
    # Primero obtener la matriz de la imagen usando la API existente
    matrix = image_to_matrix(image_path, preprocess=["grayscale", "resize_64x64"])
    
    # Parámetros para HOG
    win_size = (64, 64)
    block_size = (16, 16)
    block_stride = (8, 8)
    cell_size = (8, 8)
    nbins = 9
    
    # Extraer características HOG
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
    features = hog.compute(matrix.astype(np.uint8))
    
    return features

# Uso
features = extract_hog_features("ruta/a/imagen.jpg")
print(f"Características HOG extraídas: {features.shape}")
```

#### Ejemplo de extracción de características SIFT

```python
def extract_sift_features(image_path):
    """Extrae características SIFT de una imagen usando la API."""
    # Obtener la matriz de la imagen
    matrix = image_to_matrix(image_path, preprocess=["grayscale"])
    
    # Crear detector SIFT
    sift = cv2.SIFT_create()
    
    # Detectar keypoints y calcular descriptores
    keypoints, descriptors = sift.detectAndCompute(matrix.astype(np.uint8), None)
    
    return keypoints, descriptors

# Uso
keypoints, descriptors = extract_sift_features("ruta/a/imagen.jpg")
print(f"Número de keypoints SIFT: {len(keypoints)}")
print(f"Forma de los descriptores: {descriptors.shape}")
```

### 5. Integración con TensorFlow/PyTorch

Puedes integrar fácilmente la API con frameworks populares de aprendizaje profundo:

#### Ejemplo con TensorFlow

```python
import tensorflow as tf
import numpy as np

def load_image_batch_for_tensorflow(image_paths, preprocess=None):
    """Carga un lote de imágenes para TensorFlow usando la API."""
    # Obtener las matrices usando la API
    matrices = []
    for path in image_paths:
        matrix = image_to_matrix(
            path, 
            preprocess=["normalize", "resize_224x224"]
        )
        matrices.append(matrix)
    
    # Convertir a tensor de TensorFlow
    return tf.convert_to_tensor(np.stack(matrices))

# Uso con un modelo preentrenado
model = tf.keras.applications.MobileNetV2(weights='imagenet')
images = load_image_batch_for_tensorflow(["imagen1.jpg", "imagen2.jpg"])
predictions = model.predict(images)
```

#### Ejemplo con PyTorch

```python
import torch
import numpy as np
from torchvision import transforms

def load_image_batch_for_pytorch(image_paths, preprocess=None):
    """Carga un lote de imágenes para PyTorch usando la API."""
    # Obtener las matrices usando la API
    matrices = []
    for path in image_paths:
        matrix = image_to_matrix(
            path, 
            preprocess=["normalize", "resize_224x224"]
        )
        # Reordenar canales para PyTorch (HWC -> CHW)
        if len(matrix.shape) > 2 and matrix.shape[2] == 3:
            matrix = np.transpose(matrix, (2, 0, 1))
        matrices.append(matrix)
    
    # Convertir a tensor de PyTorch
    return torch.tensor(np.stack(matrices), dtype=torch.float32)

# Uso con un modelo preentrenado
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()
images = load_image_batch_for_pytorch(["imagen1.jpg", "imagen2.jpg"])
with torch.no_grad():
    predictions = model(images)
```

## Resolución de problemas comunes

### "API key missing"

**Problema**: Recibes un error 401 con el mensaje "API key missing".

**Solución**:

- Asegúrate de incluir la cabecera `X-API-Key` en tu solicitud
- Verifica que el nombre de la cabecera sea exactamente `X-API-Key` (distingue mayúsculas/minúsculas)

### "Invalid API key"

**Problema**: Recibes un error 403 con el mensaje "Invalid API key".

**Solución**:

- Verifica que el valor de la clave API sea correcto
- Si has cambiado la clave predeterminada en el archivo `.env`, usa ese valor

### "Error al procesar la imagen"

**Problema**: Recibes un error 500 con el mensaje "Error al procesar la imagen".

**Solución**:

- Verifica que el formato de la imagen sea compatible (JPG, PNG, BMP, TIFF)
- Asegúrate de que el tamaño del archivo no exceda el límite configurado (10MB por defecto)
- Comprueba que la imagen no esté corrupta

### Tiempos de respuesta lentos

**Problema**: Las solicitudes tardan mucho en procesarse.

**Solución**:

- Para imágenes grandes, considera redimensionarlas antes de enviarlas
- Ajusta los recursos asignados al contenedor si estás usando Docker
- Considera escalar horizontalmente el servicio añadiendo más instancias

### Fallo al ejecutar en Docker

**Problema**: El contenedor Docker falla al iniciar.

**Solución**:

- Verifica que los puertos no estén en uso (`docker ps`)
- Comprueba los logs del contenedor (`docker logs <container_id>`)
- Asegúrate de que el archivo `.env` existe si lo estás usando

### Problemas con OpenCV en diferentes plataformas

**Problema**: Errores relacionados con OpenCV cuando se ejecuta en diferentes sistemas operativos.

**Solución**:

- **Windows**: Asegúrate de tener instalado Visual C++ Redistributable
- **macOS**: Puedes necesitar instalar OpenCV vía brew: `brew install opencv`
- **Linux**: Instala las dependencias necesarias:

```bash
apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
```

### Problemas de memoria con imágenes grandes

**Problema**: Errores de memoria al procesar imágenes de gran tamaño.

**Solución**:

- Aumenta los límites de memoria en Docker:

```yaml
# En docker-compose.yml
services:
  api:
    # ...
    deploy:
      resources:
        limits:
          memory: 1G
```

- Usa el preprocesamiento para redimensionar primero:

```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -F "image=@imagen_grande.jpg" \
  -F "preprocess=resize_1024x1024"
```

## Optimizando el rendimiento

### 1. Uso de caché para operaciones repetitivas

Si estás procesando repetidamente las mismas imágenes, considera implementar un sistema de caché:

```python
import functools
import hashlib

@functools.lru_cache(maxsize=100)
def cached_image_to_matrix(image_path, preprocess=None, format="json"):
    """Versión en caché de la función image_to_matrix."""
    # Generar una clave única basada en la ruta de la imagen y las opciones
    cache_key = f"{image_path}_{preprocess}_{format}"
    cache_key = hashlib.md5(cache_key.encode()).hexdigest()
    
    # Aquí podrías verificar una caché persistente (Redis, archivo, etc.)
    
    # Si no está en caché, llamar a la API
    result = image_to_matrix(image_path, preprocess, format)
    
    # Aquí podrías guardar el resultado en una caché persistente
    
    return result
```

### 2. Procesamiento en paralelo

Para procesar múltiples imágenes simultáneamente:

```python
import concurrent.futures
import time

def process_images_in_parallel(image_paths, preprocess=None, max_workers=4):
    """Procesa varias imágenes en paralelo usando multithreading."""
    results = {}
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Crear un diccionario de futuros
        future_to_path = {
            executor.submit(image_to_matrix, path, preprocess): path
            for path in image_paths
        }
        
        # Procesar los resultados a medida que se completan
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                data = future.result()
                results[path] = data
            except Exception as exc:
                print(f"{path} generó una excepción: {exc}")
    
    elapsed = time.time() - start_time
    print(f"Procesadas {len(results)} imágenes en {elapsed:.2f} segundos")
    return results

# Uso
images = ["imagen1.jpg", "imagen2.jpg", "imagen3.jpg", "imagen4.jpg"]
results = process_images_in_parallel(images, preprocess=["grayscale", "normalize"])
```
