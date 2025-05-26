# Ejemplos y Solución de Problemas - MatrixToImage API

## Ejemplos de uso de la API

### Ejemplos en Python

```python
import requests
import numpy as np
import json
import io
from PIL import Image

# URL base de la API
BASE_URL = "http://localhost:8001"
API_KEY = "development_key_change_me"

# Función para convertir una matriz a imagen
def matrix_to_image(matrix, format="png", postprocess=None, colormap=None):
    """
    Convierte una matriz en una imagen usando la API MatrixToImage.
    
    Args:
        matrix: Matriz numpy a convertir en imagen
        format: Formato de salida ('png', 'jpg', 'bmp')
        postprocess: Lista de operaciones de postprocesamiento (opcional)
        colormap: Mapa de colores para matrices 2D (opcional)
        
    Returns:
        Objeto PIL.Image con la imagen generada
    """
    url = f"{BASE_URL}/api/v1/convert"
    
    # Preparar cabeceras
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Preparar datos
    data = {
        "matrix": matrix.tolist() if isinstance(matrix, np.ndarray) else matrix,
        "format": format
    }
    
    # Añadir postprocesamiento si se especifica
    if postprocess:
        if isinstance(postprocess, list):
            postprocess = ",".join(postprocess)
        data["postprocess"] = postprocess
    
    # Añadir mapa de colores si se especifica
    if colormap:
        data["colormap"] = colormap
    
    # Hacer la solicitud
    response = requests.post(url, headers=headers, json=data)
    
    # Comprobar si la solicitud fue exitosa
    response.raise_for_status()
    
    # Cargar la imagen desde los bytes devueltos
    return Image.open(io.BytesIO(response.content))

# Ejemplo 1: Conversión simple de matriz a PNG
matrix = np.random.rand(100, 100)  # Matriz 2D aleatoria
image = matrix_to_image(matrix)
image.save("matriz_simple.png")
print("Imagen guardada como matriz_simple.png")

# Ejemplo 2: Aplicar mapa de colores a matriz 2D
matrix_2d = np.random.rand(100, 100)
image_colored = matrix_to_image(
    matrix_2d,
    colormap="viridis"
)
image_colored.save("matriz_colormap.png")
print("Imagen guardada como matriz_colormap.png")

# Ejemplo 3: Matriz 3D (imagen RGB)
matrix_3d = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
image_rgb = matrix_to_image(matrix_3d)
image_rgb.save("matriz_rgb.png")
print("Imagen guardada como matriz_rgb.png")

# Ejemplo 4: Con postprocesamiento
matrix_noisy = np.random.rand(100, 100) * 0.5 + np.random.randn(100, 100) * 0.1
image_processed = matrix_to_image(
    matrix_noisy,
    postprocess=["normalize", "denoise"]
)
image_processed.save("matriz_procesada.png")
print("Imagen guardada como matriz_procesada.png")
```

### Ejemplos con cURL

#### Conversión simple de matriz a imagen

```bash
curl -X POST \
  http://localhost:8001/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -H "Content-Type: application/json" \
  -d '{
    "matrix": [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
    "format": "png"
  }' \
  --output imagen.png
```

#### Con mapa de colores

```bash
curl -X POST \
  http://localhost:8001/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -H "Content-Type: application/json" \
  -d '{
    "matrix": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
    "format": "png",
    "colormap": "plasma"
  }' \
  --output imagen_colormap.png
```

#### Con postprocesamiento

```bash
curl -X POST \
  http://localhost:8001/api/v1/convert \
  -H "X-API-Key: development_key_change_me" \
  -H "Content-Type: application/json" \
  -d '{
    "matrix": [[50, 100, 150], [200, 250, 300], [350, 400, 450]],
    "format": "jpg",
    "postprocess": "normalize,equalize"
  }' \
  --output imagen_procesada.jpg
```

### Ejemplos con Postman

1. Crea una nueva solicitud POST a `http://localhost:8001/api/v1/convert`

2. En la pestaña "Headers", añade:
   - Key: `X-API-Key`
   - Value: `development_key_change_me`
   - Key: `Content-Type`
   - Value: `application/json`

3. En la pestaña "Body":
   - Selecciona "raw" y "JSON"
   - Introduce un objeto JSON como este:
     ```json
     {
       "matrix": [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
       "format": "png",
       "colormap": "viridis"
     }
     ```

4. En "Settings":
   - Marca "Send as binary" para descargar la imagen

5. Envía la solicitud y guarda la respuesta como imagen

## Casos de uso comunes

### 1. Visualización de datos numéricos

```python
import numpy as np
import matplotlib.pyplot as plt

# Crear datos de ejemplo (matrix)
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Visualizar con MatrixToImage API
image = matrix_to_image(Z, colormap="viridis")
image.save("visualization.png")

# Comparación con visualización directa de matplotlib
plt.figure(figsize=(8, 6))
plt.imshow(Z, cmap='viridis')
plt.colorbar()
plt.savefig("matplotlib_direct.png")
```

### 2. Visualización de matrices complejas

```python
def visualize_complex_matrix(complex_matrix, output_path):
    """Visualiza una matriz de números complejos usando la amplitud y fase."""
    # Extraer amplitud y fase
    amplitude = np.abs(complex_matrix)
    phase = np.angle(complex_matrix)
    
    # Normalizar amplitud para visualización
    amplitude_norm = amplitude / np.max(amplitude)
    
    # Convertir a imágenes usando la API
    amplitude_img = matrix_to_image(amplitude_norm, colormap="inferno")
    phase_img = matrix_to_image((phase + np.pi) / (2 * np.pi), colormap="hsv")
    
    # Guardar las imágenes
    amplitude_img.save(f"{output_path}_amplitude.png")
    phase_img.save(f"{output_path}_phase.png")
    
    return amplitude_img, phase_img

# Ejemplo de uso con transformada de Fourier
# Crear una imagen de prueba
test_image = np.zeros((100, 100))
test_image[30:70, 30:70] = 1  # Cuadrado en el centro

# Calcular la transformada de Fourier
fft_result = np.fft.fft2(test_image)
fft_shifted = np.fft.fftshift(fft_result)  # Centrar las frecuencias

# Visualizar
amplitude_img, phase_img = visualize_complex_matrix(fft_shifted, "fft_result")
```

### 3. Generación de mapas de calor a partir de datos

```python
def generate_heatmap(data, x_labels=None, y_labels=None, colormap="inferno"):
    """
    Genera un mapa de calor a partir de datos matriciales.
    
    Args:
        data: Matriz 2D con los valores
        x_labels: Etiquetas para el eje X
        y_labels: Etiquetas para el eje Y
        colormap: Mapa de colores para la visualización
    """
    # Convertir a array numpy si no lo es
    data_array = np.array(data)
    
    # Obtener imagen base usando la API
    heatmap_img = matrix_to_image(
        data_array, 
        colormap=colormap,
        postprocess="normalize"
    )
    
    # Si se requiere una imagen con ejes y etiquetas:
    # (Este ejemplo usa matplotlib directamente, pero podrías generar la imagen
    # con MatrixToImage y luego añadir las etiquetas con Pillow)
    if x_labels is not None or y_labels is not None:
        plt.figure(figsize=(10, 8))
        plt.imshow(data_array, cmap=colormap)
        plt.colorbar(label="Valor")
        
        # Configurar ejes y etiquetas si se proporcionan
        if x_labels:
            plt.xticks(range(len(x_labels)), x_labels, rotation=45)
        if y_labels:
            plt.yticks(range(len(y_labels)), y_labels)
            
        plt.tight_layout()
        plt.savefig("heatmap_with_labels.png")
    
    return heatmap_img

# Ejemplo: Mapa de calor de correlación
np.random.seed(42)
data = np.random.randn(50, 5)
correlation_matrix = np.corrcoef(data.T)

variables = ['Var A', 'Var B', 'Var C', 'Var D', 'Var E']
heatmap = generate_heatmap(
    correlation_matrix,
    x_labels=variables,
    y_labels=variables,
    colormap="coolwarm"
)
heatmap.save("correlation_heatmap.png")
```

### 4. Visualización de datos de aprendizaje automático

```python
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE

# Cargar el conjunto de datos MNIST de dígitos
digits = load_digits()
X = digits.data
y = digits.target

# Reducir dimensionalidad con t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_embedded = tsne.fit_transform(X)

# Crear una matriz 2D para visualizar
grid_size = 500
grid = np.zeros((grid_size, grid_size))

# Normalizar las coordenadas al tamaño de la cuadrícula
X_norm = (X_embedded - X_embedded.min(axis=0)) / (X_embedded.max(axis=0) - X_embedded.min(axis=0))
X_norm = (X_norm * (grid_size - 1)).astype(int)

# Crear visualización de densidad
for x, y_val in X_norm:
    grid[y_val, x] += 1

# Suavizar los resultados
from scipy.ndimage import gaussian_filter
grid_smooth = gaussian_filter(grid, sigma=3)

# Visualizar usando MatrixToImage
density_img = matrix_to_image(
    grid_smooth,
    colormap="viridis",
    postprocess="normalize"
)
density_img.save("tsne_density.png")
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

### "Formato de la matriz no válido"

**Problema**: Recibes un error 400 sobre el formato de la matriz.

**Solución**:

- Asegúrate de que tu matriz sea 2D o 3D
- Para matrices 2D: valores numéricos en una matriz de forma [altura, anchura]
- Para matrices 3D (RGB): valores en forma [altura, anchura, 3] con valores entre 0-255 para cada canal
- Verifica que la matriz no contenga valores NaN o infinitos
- Asegúrate de que los tipos de datos sean numéricos (enteros o flotantes)

### "Error al procesar la matriz"

**Problema**: Recibes un error 500 con el mensaje "Error al procesar la matriz".

**Solución**:

- Verifica que el tamaño de la matriz no exceda el límite configurado (MAX_MATRIX_SIZE)
- Comprueba que la matriz no tenga valores extremadamente grandes o pequeños
- Si estás usando tipos de datos especiales, conviértelos a tipos estándar (int o float)

### "JSONDecodeError"

**Problema**: Tu petición falla con un error de decodificación JSON.

**Solución**:

- Asegúrate de que tu payload JSON sea válido
- Verifica que estés usando `Content-Type: application/json` en las cabeceras
- Si tu matriz es grande, considera partirla en partes más pequeñas

### Problemas con la visualización de mapas de colores

**Problema**: El mapa de colores no se aplica correctamente a tu matriz 2D.

**Solución**:

- Asegúrate de que tu matriz sea realmente 2D ([altura, anchura]) y no 3D
- Verifica que estés usando un nombre de mapa de colores válido
- Considera normalizar tus datos al rango [0, 1] antes de enviarlos:
  ```python
  if matrix.max() > matrix.min():
      matrix = (matrix - matrix.min()) / (matrix.max() - matrix.min())
  ```

### La imagen generada está distorsionada

**Problema**: La imagen generada no representa correctamente los datos.

**Solución**:

- Para matrices 2D: Asegúrate de que la forma sea la esperada (filas × columnas)
- Para matrices 3D: Verifica que el último índice sea 3 (para RGB)
- Considera aplicar `postprocess=normalize` para optimizar el rango dinámico

### Problemas de falta de memoria

**Problema**: El servicio se queda sin memoria al procesar matrices muy grandes.

**Solución**:

- Reduce el tamaño de tu matriz antes de enviarla
- Considera submuestrear tus datos si no necesitas la resolución completa
- Si es posible, divide la matriz en bloques más pequeños y procésalos por separado

## Optimizando el rendimiento

### 1. Reducción del tamaño de los datos

Para optimizar el rendimiento cuando se trabaja con matrices muy grandes:

```python
def downsample_matrix(matrix, factor):
    """Reduce el tamaño de una matriz por un factor dado."""
    if matrix.ndim == 2:
        return matrix[::factor, ::factor]
    elif matrix.ndim == 3:
        return matrix[::factor, ::factor, :]
    else:
        raise ValueError("La matriz debe ser 2D o 3D")

# Ejemplo
large_matrix = np.random.rand(1000, 1000)
downsampled = downsample_matrix(large_matrix, 4)  # Reduce a 250x250
image = matrix_to_image(downsampled, colormap="viridis")
```

### 2. Procesamiento por lotes

Para procesar múltiples matrices:

```python
import concurrent.futures
import time

def process_matrices_in_parallel(matrices, max_workers=4, **kwargs):
    """Procesa múltiples matrices en paralelo."""
    results = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Crear un mapa de matrices a futuros
        future_to_matrix = {
            executor.submit(matrix_to_image, matrix, **kwargs): i
            for i, matrix in enumerate(matrices)
        }
        
        # Procesar los resultados a medida que se completan
        for future in concurrent.futures.as_completed(future_to_matrix):
            idx = future_to_matrix[future]
            try:
                image = future.result()
                results.append((idx, image))
            except Exception as exc:
                print(f"La matriz {idx} generó un error: {exc}")
    
    # Ordenar los resultados por índice original
    results.sort(key=lambda x: x[0])
    
    elapsed = time.time() - start_time
    print(f"Procesadas {len(results)} matrices en {elapsed:.2f} segundos")
    
    # Devolver solo las imágenes, manteniendo el orden original
    return [img for _, img in results]

# Ejemplo de uso
matrices = [np.random.rand(100, 100) for _ in range(10)]
images = process_matrices_in_parallel(
    matrices, 
    max_workers=4,
    colormap="viridis"
)

# Guardar las imágenes resultantes
for i, img in enumerate(images):
    img.save(f"matriz_{i}.png")
```

### 3. Compresión de imágenes para respuestas más rápidas

```python
def optimize_image_size(image, format="JPEG", quality=85):
    """Optimiza el tamaño de una imagen para transferencia más rápida."""
    from io import BytesIO
    
    buffer = BytesIO()
    image.save(buffer, format=format, quality=quality, optimize=True)
    buffer.seek(0)
    return Image.open(buffer)

# Ejemplo
matrix = np.random.rand(500, 500)
image = matrix_to_image(matrix, colormap="plasma")
optimized = optimize_image_size(image, format="JPEG", quality=90)
optimized.save("optimized.jpg")

# Comparar tamaños
print(f"Tamaño original: {image.size[0]}x{image.size[1]}")
print(f"Tamaño optimizado: {optimized.size[0]}x{optimized.size[1]}")
```

### 4. Caching de resultados frecuentes

```python
import functools
import hashlib

@functools.lru_cache(maxsize=100)
def cached_matrix_to_image(matrix_tuple, **kwargs):
    """Versión en caché de la función matrix_to_image."""
    # Convertir la tupla de vuelta a un array numpy
    shape, dtype, data = matrix_tuple
    matrix = np.array(data).reshape(shape).astype(dtype)
    
    # Llamar a la función original
    return matrix_to_image(matrix, **kwargs)

def matrix_to_image_with_cache(matrix, **kwargs):
    """Wrapper que prepara la matriz para caché y llama a la función en caché."""
    # Convertir la matriz a una forma hasheable (tupla)
    matrix_tuple = (matrix.shape, str(matrix.dtype), tuple(matrix.flatten()))
    
    # Llamar a la versión en caché
    return cached_matrix_to_image(matrix_tuple, **kwargs)

# Ejemplo de uso
matrix = np.random.rand(100, 100)
# Primera llamada (no en caché)
image1 = matrix_to_image_with_cache(matrix, colormap="viridis")
# Segunda llamada (desde caché)
image2 = matrix_to_image_with_cache(matrix, colormap="viridis")
```
