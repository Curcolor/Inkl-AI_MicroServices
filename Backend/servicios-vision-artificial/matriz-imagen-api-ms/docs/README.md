# Documentación de MatrixToImage API

## Descripción General

MatrixToImage es una API para convertir matrices numéricas a imágenes para su visualización y uso posterior. La API está diseñada como un microservicio independiente que puede integrarse fácilmente en una arquitectura de microservicios más grande.

## Documentación adicional

- [Ejemplos de uso y solución de problemas](examples_and_troubleshooting.md)

## Arquitectura

El proyecto sigue una arquitectura en capas:

```
MatrixToImage/
├── src/                  # Código fuente principal
│   ├── api/              # Endpoints de la API y controladores
│   ├── services/         # Lógica de negocio
│   ├── utils/            # Utilidades
│   └── config/           # Configuración
```

### Componentes Principales

1. **API Layer**: Gestiona las peticiones HTTP entrantes y las respuestas.
2. **Service Layer**: Contiene la lógica de negocio para la generación de imágenes a partir de matrices.
3. **Utilities**: Funciones auxiliares para el procesamiento y la validación.
4. **Configuration**: Gestión de configuraciones y variables de entorno.

## Endpoints

Esta API ofrece los siguientes endpoints para interactuar con el servicio de conversión de matrices a imágenes.

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
curl -X GET http://localhost:8001/health
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
Convierte una matriz numérica a una imagen. Este es el endpoint principal del servicio que permite transformar representaciones matriciales en archivos de imagen que pueden ser visualizados o utilizados posteriormente.

#### URL
```
POST http://host:puerto/api/v1/convert
```

#### Cabeceras requeridas
| Cabecera | Descripción | Obligatorio |
|----------|-------------|-------------|
| X-API-Key | Clave de autenticación para acceder a la API | Sí |

#### Parámetros (JSON)
| Parámetro | Tipo | Descripción | Obligatorio | Valores posibles |
|-----------|------|-------------|-------------|------------------|
| matrix | Array | Matriz numérica a convertir en imagen | Sí | Matriz 2D (escala de grises) o 3D (color) |
| format | String | Formato de la imagen de salida | No | `png` (predeterminado), `jpg`, `bmp` |
| postprocess | String | Lista de operaciones de postprocesamiento separadas por comas | No | `normalize`, `equalize`, `denoise` |
| colormap | String | Mapa de colores a aplicar para matrices 2D | No | `viridis`, `plasma`, `inferno`, `magma`, `cividis` |

#### Opciones de postprocesamiento detalladas

##### `normalize`
Normaliza los valores de los píxeles para utilizar todo el rango disponible (0-255). Especialmente útil para matrices con valores en rangos no estándar.

**Efectos en la imagen resultante:**
- Mejora del contraste
- Optimización del rango dinámico

##### `equalize`
Aplica ecualización de histograma para mejorar el contraste y la distribución de intensidades.

**Efectos en la imagen resultante:**
- Mejor contraste global
- Mejor detalle en áreas con poco contraste

##### `denoise`
Aplica algoritmos de reducción de ruido a la imagen generada.

**Efectos en la imagen resultante:**
- Reducción de artefactos
- Suavizado de ruido manteniendo los bordes

#### Mapas de colores para matrices 2D

Para matrices bidimensionales (escala de grises), se puede aplicar un mapa de colores para generar una representación visual en color:

| Mapa de colores | Descripción |
|-----------------|-------------|
| `viridis` | Paleta de azul a amarillo, perceptualmente uniforme y visible para personas con daltonismo |
| `plasma` | Paleta violeta a amarillo, alta diferenciación |
| `inferno` | Paleta de negro a amarillo, alto contraste |
| `magma` | Paleta de negro a rosa claro |
| `cividis` | Paleta optimizada para visión con daltonismo |

#### Ejemplos de solicitud

**Solicitud básica:**
```bash
curl -X POST \
  http://localhost:8001/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -H 'Content-Type: application/json' \
  -d '{
    "matrix": [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
    "format": "png"
  }'
```

**Con mapa de colores:**
```bash
curl -X POST \
  http://localhost:8001/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -H 'Content-Type: application/json' \
  -d '{
    "matrix": [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
    "format": "png",
    "colormap": "viridis"
  }'
```

**Con postprocesamiento:**
```bash
curl -X POST \
  http://localhost:8001/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -H 'Content-Type: application/json' \
  -d '{
    "matrix": [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
    "format": "jpg",
    "postprocess": "normalize,denoise"
  }'
```

#### Respuestas posibles

##### Éxito (200 OK)
Devuelve la imagen en el formato solicitado con tipo de contenido correspondiente (image/png, image/jpeg, etc.).

##### Error de validación (400 Bad Request)
```json
{
  "detail": "Formato de la matriz no válido. Debe ser 2D o 3D."
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
  "detail": "Error al procesar la matriz: [mensaje específico del error]"
}
```

#### Límites y restricciones
- **Tamaño máximo de matriz**: 100MB (configurable mediante MAX_MATRIX_SIZE)
- **Formatos de salida permitidos**: PNG, JPG, BMP
- **Dimensiones máximas**: Configurables mediante entorno

## Implementación técnica

### Procesamiento de imágenes

El servicio utiliza una combinación de bibliotecas populares para la generación y procesamiento de imágenes:

#### Pillow (PIL)
- Generación de imágenes
- Manipulación básica de imágenes
- Conversión entre formatos

#### NumPy
- Manipulación eficiente de matrices
- Operaciones vectorizadas para mejor rendimiento
- Interpretación de datos matriciales

#### Matplotlib
- Generación de visualizaciones a partir de matrices
- Aplicación de mapas de colores
- Herramientas avanzadas de visualización

### Flujo de procesamiento interno

1. **Recepción de la matriz**: El controlador recibe los datos JSON y valida su formato.
2. **Conversión a NumPy**: Se convierte la estructura de datos recibida en una matriz NumPy.
3. **Validación de dimensiones**: Se verifica que la matriz tenga las dimensiones adecuadas.
4. **Generación de imagen**: Se crea una imagen a partir de la matriz.
5. **Postprocesamiento**: Se aplican las operaciones solicitadas.
6. **Formateo de respuesta**: Se devuelve la imagen en el formato solicitado.

### Optimización de rendimiento

- **Caché LRU**: Implementada para la configuración del servicio
- **Procesamiento asíncrono**: Uso de FastAPI/asyncio para manejo de múltiples peticiones
- **Gestión eficiente de memoria**: Liberación de recursos después del procesamiento

## Guía de integración con otros sistemas

### Integración como Microservicio

Para integrar esta API en una arquitectura de microservicios:

#### 1. Configuración con Docker

El proyecto incluye configuración completa para Docker:

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias para procesamiento de imágenes
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
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]
```

**docker-compose.yml**:
```yaml
version: '3'

services:
  matrix-to-imagen:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8001
      - DEBUG=True
      - LOG_LEVEL=INFO
      - DEFAULT_API_KEY=development_key_change_me
      # Adaptar si ImageToMatrix está en otro servicio o contenedor
      - IMAGE_TO_MATRIX_URL=http://host.docker.internal:8000/api/v1/convert
    volumes:
      - ./src:/app/src  # Para desarrollo, habilita cambios en tiempo real
    networks:
      - matrix_network

networks:
  matrix_network:
    driver: bridge
```

#### 2. Configuración con Variables de Entorno

La API utiliza variables de entorno para su configuración. Puedes proporcionar estas variables directamente o a través de un archivo `.env`:

```bash
# Archivo .env
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=False
LOG_LEVEL=INFO
MAX_MATRIX_SIZE=104857600
API_KEY_HEADER=X-API-Key
DEFAULT_API_KEY=tu_clave_api_segura
```

#### 3. Uso del Health Check

El endpoint `/health` está diseñado para ser utilizado por monitores de salud como Kubernetes liveness probes, balanceadores de carga o servicios de monitoreo.

#### 4. Integración con API Gateway

Este servicio se puede integrar fácilmente con cualquier API Gateway que soporte autenticación por cabeceras.

### Seguridad

El servicio implementa varias medidas de seguridad:

#### 1. Autenticación mediante API Key

Todas las peticiones a `/api/v1/convert` requieren una cabecera `X-API-Key` con un valor válido.

#### 2. Validación de entrada

- Verificación de formato y dimensiones de matriz
- Limitación de tamaño máximo de matriz
- Restricción de parámetros válidos

#### 3. Prácticas de seguridad recomendadas

- **Cambiar la clave API predeterminada** en producción
- **Usar HTTPS** (configurar un proxy inverso como Nginx)
- **Aplicar rate limiting** para prevenir ataques de denegación de servicio

### Monitorización y diagnóstico

El servicio incluye capacidades de monitorización y logging para facilitar el diagnóstico de problemas y el seguimiento del rendimiento en entornos de producción.
