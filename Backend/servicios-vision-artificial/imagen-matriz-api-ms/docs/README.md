# Documentación de ImageToMatrix API

## Descripción General

ImageToMatrix es una API para convertir imágenes a matrices numéricas para su procesamiento posterior. La API está diseñada como un microservicio independiente que puede integrarse fácilmente en una arquitectura de microservicios más grande.

## Documentación adicional

- [Ejemplos de uso y solución de problemas](examples_and_troubleshooting.md)

## Arquitectura

El proyecto sigue una arquitectura en capas:

```
ImageToMatrix/
├── src/                  # Código fuente principal
│   ├── api/              # Endpoints de la API y controladores
│   ├── services/         # Lógica de negocio
│   ├── utils/            # Utilidades
│   └── config/           # Configuración
```

### Componentes Principales

1. **API Layer**: Gestiona las peticiones HTTP entrantes y las respuestas.
2. **Service Layer**: Contiene la lógica de negocio para el procesamiento de imágenes.
3. **Utilities**: Funciones auxiliares para el procesamiento y la validación.
4. **Configuration**: Gestión de configuraciones y variables de entorno.

## Endpoints

Esta API ofrece los siguientes endpoints para interactuar con el servicio de conversión de imágenes a matrices.

### `GET /health`

#### Descripción
Comprueba si la API está funcionando correctamente. Este endpoint es útil para implementaciones de monitoreo, balanceadores de carga y verificaciones de disponibilidad.

#### URL
```
GET http://host:puerto/health
```

#### Parámetros
No requiere parámetros.

#### Cabeceras
No requiere cabeceras específicas.

#### Ejemplo de solicitud
```bash
curl -X GET http://localhost:8000/health
```

#### Respuestas posibles

##### Éxito (200 OK)
```json
{
  "status": "healthy"
}
```

##### Error del servidor (500 Internal Server Error)
```json
{
  "detail": "El servicio no está disponible temporalmente"
}
```

### `POST /api/v1/convert`

#### Descripción
Convierte una imagen a una matriz numérica. Este es el endpoint principal del servicio que permite transformar archivos de imagen en representaciones matriciales que pueden ser utilizadas para procesamiento o análisis posterior.

#### URL
```
POST http://host:puerto/api/v1/convert
```

#### Cabeceras requeridas
| Cabecera | Descripción | Obligatorio |
|----------|-------------|-------------|
| X-API-Key | Clave de autenticación para acceder a la API | Sí |

#### Parámetros (form-data)
| Parámetro | Tipo | Descripción | Obligatorio | Valores posibles |
|-----------|------|-------------|-------------|------------------|
| image | File | Archivo de imagen a convertir | Sí | Archivos JPG, JPEG, PNG, BMP, TIFF (máx. 10MB por defecto) |
| format | String | Formato en el que se devolverá la matriz | No | `json` (predeterminado), `numpy` |
| preprocess | String | Lista de operaciones de preprocesamiento separadas por comas | No | `grayscale`, `normalize`, `resize_WxH` |

#### Opciones de preprocesamiento detalladas

##### `grayscale`
Convierte la imagen a escala de grises. Esto reduce la matriz resultante a un solo canal por píxel en lugar de los tres canales RGB.

**Efectos en la matriz resultante:**
- Dimensión de la matriz: `[alto, ancho]` en lugar de `[alto, ancho, 3]`
- Valores: Representan la intensidad en escala de grises (0-255 o 0-1 si se normaliza)

##### `normalize`
Normaliza los valores de los píxeles al rango [0, 1] dividiendo cada valor por 255. Esto es útil para el procesamiento posterior, especialmente para modelos de aprendizaje automático.

**Efectos en la matriz resultante:**
- Rango de valores: De 0.0 a 1.0 en lugar de 0 a 255
- Tipo de datos: float32 en lugar de uint8

##### `resize_WxH`
Redimensiona la imagen a las dimensiones especificadas (ancho × alto). Por ejemplo, `resize_224x224` redimensionará la imagen a 224×224 píxeles.

**Parámetros:**
- W: Ancho deseado en píxeles
- H: Alto deseado en píxeles

**Efectos en la matriz resultante:**
- Dimensiones: `[H, W]` o `[H, W, canales]`, según si se aplica escala de grises
- Algoritmo: Utiliza interpolación de área (LANCZOS) para mantener la calidad

#### Procesamiento combinado
Los parámetros de preprocesamiento pueden combinarse. Por ejemplo:
```
preprocess=grayscale,normalize,resize_224x224
```

Esta combinación:
1. Primero convierte la imagen a escala de grises
2. Luego normaliza los valores al rango [0, 1]
3. Finalmente redimensiona la imagen a 224×224 píxeles

#### Ejemplos de solicitud

**Solicitud básica:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -F 'image=@/ruta/a/imagen.jpg'
```

**Con formato específico:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -F 'image=@/ruta/a/imagen.jpg' \
  -F 'format=json'
```

**Con preprocesamiento:**
```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -F 'image=@/ruta/a/imagen.jpg' \
  -F 'preprocess=grayscale,normalize,resize_224x224'
```

#### Respuestas posibles

##### Éxito (200 OK) - Formato JSON
```json
{
  "matrix": [[[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]], [[0.7, 0.8, 0.9], [0.4, 0.5, 0.6]]],
  "shape": [2, 2, 3],
  "dtype": "float32"
}
```

##### Éxito (200 OK) - Formato NumPy
Devuelve un archivo binario con la matriz serializada en formato NumPy (.npy).

##### Error de validación (400 Bad Request)
```json
{
  "detail": "Formato de imagen no compatible. Formatos permitidos: jpg, jpeg, png, bmp, tiff"
}
```

##### Error de autenticación (401 Unauthorized)
```json
{
  "detail": "API key missing"
}
```

##### Error de permisos (403 Forbidden)
```json
{
  "detail": "Invalid API key"
}
```

##### Error de procesamiento (500 Internal Server Error)
```json
{
  "detail": "Error al procesar la imagen: [mensaje específico del error]"
}
```

#### Límites y restricciones
- **Tamaño máximo de archivo**: 10MB (configurable mediante MAX_IMAGE_SIZE)
- **Formatos permitidos**: JPG, JPEG, PNG, BMP, TIFF (configurable mediante ALLOWED_EXTENSIONS)
- **Dimensiones máximas**: 2048×2048 píxeles (configurable mediante MAX_WIDTH y MAX_HEIGHT)

## Implementación técnica

### Procesamiento de imágenes

El servicio utiliza una combinación de bibliotecas populares para el procesamiento de imágenes:

#### Pillow (PIL)
- Apertura y manipulación básica de imágenes
- Conversión entre formatos
- Redimensionamiento básico

#### NumPy
- Manipulación eficiente de matrices
- Operaciones vectorizadas para mejor rendimiento
- Serialización de matrices para el formato de salida

#### OpenCV
- Procesamiento avanzado de imágenes
- Extracción de características (HOG, SIFT, ORB)
- Operaciones de alto rendimiento

### Flujo de procesamiento interno

1. **Recepción de la imagen**: El controlador recibe el archivo y valida su formato y tamaño.
2. **Lectura del contenido**: Se lee el archivo como un stream de bytes.
3. **Conversión a objeto PIL**: Se crea un objeto `Image` usando Pillow.
4. **Preprocesamiento**: Se aplican las operaciones solicitadas en el siguiente orden:
   - Conversión a escala de grises (si se solicita)
   - Redimensionamiento (si se solicita)
   - Normalización (si se solicita)
5. **Conversión a matriz NumPy**: Se transforma la imagen en una matriz n-dimensional.
6. **Formateo de respuesta**: Se devuelve la matriz en el formato solicitado.

### Optimización de rendimiento

- **Caché LRU**: Implementada para la configuración del servicio
- **Procesamiento asíncrono**: Uso de FastAPI/asyncio para manejo de múltiples peticiones
- **Gestión eficiente de memoria**: Liberación de recursos después del procesamiento

### Extracción de características avanzadas

El servicio puede extraer características avanzadas de imágenes mediante el módulo `ImageProcessingUtils`:

#### HOG (Histograma de Gradientes Orientados)
```python
# Ejemplo de uso interno
from src.utils.image_processing import ImageProcessingUtils
features = ImageProcessingUtils.extract_image_features(matrix, feature_type="hog")
```

#### SIFT (Scale-Invariant Feature Transform)
```python
features = ImageProcessingUtils.extract_image_features(matrix, feature_type="sift")
```

#### ORB (Oriented FAST and Rotated BRIEF)
```python
features = ImageProcessingUtils.extract_image_features(matrix, feature_type="orb")
```

## Guía de integración con otros sistemas

### Integración como Microservicio

Para integrar esta API en una arquitectura de microservicios:

#### 1. Configuración con Docker

El proyecto incluye configuración completa para Docker:

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias para OpenCV y Pillow
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto usado por la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health", "||", "exit", "1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

#### 2. Configuración con Variables de Entorno

La API utiliza variables de entorno para su configuración. Puedes proporcionar estas variables directamente o a través de un archivo `.env`:

```bash
# Archivo .env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
LOG_LEVEL=INFO
MAX_IMAGE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,bmp,tiff
API_KEY_HEADER=X-API-Key
DEFAULT_API_KEY=tu_clave_api_segura
```

#### 3. Uso del Health Check

El endpoint `/health` está diseñado para ser utilizado por monitores de salud como Kubernetes liveness probes, balanceadores de carga o servicios de monitoreo:

```yaml
# Ejemplo en Kubernetes
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

#### 4. Integración con API Gateway

El servicio se puede integrar con cualquier API Gateway que soporte autenticación por cabeceras:

**Ejemplo con Kong API Gateway**:
```bash
# Crear un servicio en Kong
curl -X POST http://kong:8001/services/ \
  --data name=imagetomatrix \
  --data url=http://imagetomatrix:8000

# Crear una ruta
curl -X POST http://kong:8001/services/imagetomatrix/routes \
  --data "paths[]=/convert" \
  --data "strip_path=false"

# Configurar plugin de autenticación de clave
curl -X POST http://kong:8001/services/imagetomatrix/plugins \
  --data name=key-auth \
  --data config.key_names=X-API-Key
```

### Escalabilidad

La API está diseñada para ser escalada horizontalmente debido a sus características:

#### 1. Arquitectura Stateless

El servicio no mantiene estado entre peticiones, lo que permite ejecutar múltiples instancias sin problemas de coherencia de datos.

#### 2. Opciones de Containerización

**Kubernetes**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: imagetomatrix
spec:
  replicas: 3
  selector:
    matchLabels:
      app: imagetomatrix
  template:
    metadata:
      labels:
        app: imagetomatrix
    spec:
      containers:
      - name: imagetomatrix
        image: imagetomatrix:latest
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "0.5"
            memory: "256Mi"
        ports:
        - containerPort: 8000
```

**Docker Swarm**:
```bash
docker service create \
  --name imagetomatrix \
  --replicas 3 \
  --publish 8000:8000 \
  imagetomatrix:latest
```

#### 3. Configuración Externalizada

Toda la configuración se puede modificar sin necesidad de reconstruir la imagen, facilitando la implementación en diferentes entornos.

### Seguridad

El servicio implementa varias medidas de seguridad:

#### 1. Autenticación mediante API Key

Todas las peticiones a `/api/v1/convert` requieren una cabecera `X-API-Key` con un valor válido.

#### 2. Validación de entrada

- Verificación de tipo MIME de los archivos
- Limitación de tamaño máximo de archivo
- Restricción de extensiones permitidas

#### 3. Prácticas de seguridad recomendadas

- **Cambiar la clave API predeterminada** en producción
- **Usar HTTPS** (configurar un proxy inverso como Nginx)
- **Aplicar rate limiting** para prevenir ataques de denegación de servicio

### Monitorización y diagnóstico

#### 1. Sistema de Logging

El servicio registra información detallada de cada petición a través de un middleware personalizado:

```
2025-05-19 10:15:32 - INFO - Request: POST /api/v1/convert
2025-05-19 10:15:33 - INFO - Response: POST /api/v1/convert - Status: 200 - Processed in: 0.8532s
```

#### 2. Métricas de rendimiento

Cada respuesta HTTP incluye una cabecera `X-Process-Time` con el tiempo de procesamiento en segundos.

#### 3. Integración con herramientas de monitoreo

El servicio es compatible con:

- **Prometheus**: Para recolección de métricas
- **Grafana**: Para visualización de dashboards
- **ELK Stack**: Para análisis de logs
- **Datadog**: Para monitoreo APM

**Ejemplo de configuración para Prometheus**:
```yaml
scrape_configs:
  - job_name: 'imagetomatrix'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['imagetomatrix:8000']
```
