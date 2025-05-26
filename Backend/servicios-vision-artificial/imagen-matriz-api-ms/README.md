# ImageToMatrix

Un microservicio para convertir imágenes en matrices numéricas optimizadas para el entrenamiento de redes neuronales convolucionales (CNN) y otras tareas de procesamiento. Diseñado para ser reutilizable, eficiente y fácil de integrar en arquitecturas de microservicios.

## Descripción

Este microservicio proporciona una API REST para convertir imágenes en diferentes formatos a matrices numéricas que pueden ser utilizadas para análisis, procesamiento o como entrada para modelos de aprendizaje automático. El proyecto está estructurado siguiendo las mejores prácticas para el desarrollo de microservicios, lo que facilita su despliegue, escalabilidad y mantenimiento.

## Características

- Conversión de imágenes a matrices numéricas (numpy arrays)
- Soporte para múltiples formatos de imagen (JPG, PNG, BMP, etc.)
- Opciones de preprocesamiento (redimensionamiento, normalización, escala de grises)
- Respuestas en diversos formatos (JSON, NumPy serializado)
- Extracción de características usando algoritmos como HOG, SIFT y ORB

## Arquitectura

Este proyecto sigue una arquitectura en capas diseñada para facilitar su implementación como microservicio:

```
ImageToMatrix/
├── src/                  # Código fuente principal
│   ├── api/              # Endpoints de la API y controladores
│   ├── services/         # Lógica de negocio
│   ├── utils/            # Utilidades
│   └── config/           # Configuración
├── tests/                # Tests
├── docs/                 # Documentación
```

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Docker y Docker Compose (opcional, para despliegue containerizado)
- Librerías de sistema para OpenCV (en Linux: libgl1-mesa-glx, libglib2.0-0)

## Instalación

### Método 1: Instalación directa

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/ImageToMatrix.git
cd ImageToMatrix

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar el paquete en modo desarrollo
pip install -e .

# Variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### Método 2: Instalación con Docker

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/ImageToMatrix.git
cd ImageToMatrix

# Copiar y modificar las variables de entorno (opcional)
cp .env.example .env

# Construir y ejecutar con docker-compose
docker-compose up -d
```

## Uso

### Ejecución local

```bash
# Método 1: Directamente con uvicorn
uvicorn src.api.app:app --reload

# Método 2: Usando el módulo instalado
python -m src.api.app

# Método 3: Ejecutar scripts incluidos (Windows)
run_tests.bat  # Para ejecutar las pruebas
```

### Con Docker

```bash
# Método 1: Utilizando scripts incluidos
# En Windows:
run_docker.bat

# En Linux/macOS:
bash run_docker.sh

# Método 2: Usando docker-compose
docker-compose up -d

# Método 3: Manual
docker build -t imagetomatrix .
docker run -p 8000:8000 imagetomatrix
```

### Verificar que el servicio está funcionando

```bash
# Comprueba el estado de salud de la API
curl http://localhost:8000/health

# Deberías ver:
# {"status":"healthy"}
```

## Endpoints

La API proporciona los siguientes endpoints:

### GET /health

**Descripción**: Comprueba el estado de la API.

**Ejemplo de uso**:
```bash
curl http://localhost:8000/health
```

**Respuesta exitosa**:
```json
{
  "status": "healthy"
}
```

### POST /api/v1/convert

**Descripción**: Convierte una imagen a una matriz numérica.

**Headers requeridos**:
- `X-API-Key`: Clave de autenticación API (valor predeterminado: `development_key_change_me`)

**Parámetros form-data**:
| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| image | File | Archivo de imagen a convertir | Sí |
| format | Text | Formato de salida (`json` o `numpy`) | No (default: `json`) |
| preprocess | Text | Opciones de preprocesamiento separadas por comas | No |

**Opciones de preprocesamiento**:
- `grayscale`: Convierte la imagen a escala de grises
- `normalize`: Normaliza los valores de píxeles (0-1)
- `resize_WxH`: Redimensiona la imagen (ejemplo: `resize_224x224`)

**Ejemplo de uso**:
```bash
curl -X POST \
  http://localhost:8000/api/v1/convert \
  -H 'X-API-Key: development_key_change_me' \
  -F 'image=@/path/to/your/image.jpg' \
  -F 'format=json' \
  -F 'preprocess=grayscale,normalize'
```

**Respuesta exitosa** (formato JSON):
```json
{
  "matrix": [[[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]], [[0.7, 0.8, 0.9], [0.4, 0.5, 0.6]]],
  "shape": [2, 2, 3],
  "dtype": "float32"
}
```

### Documentación de la API

Una vez iniciado el servicio, puedes acceder a la documentación interactiva en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Para más información detallada sobre los endpoints, consulta la [documentación completa](docs/README.md).

## Pruebas

El proyecto incluye pruebas unitarias e integración. Para ejecutarlas:

```bash
# Instalar pytest y pytest-asyncio si aún no están instalados
pip install pytest pytest-asyncio

# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas unitarias
pytest tests/unit

# Ejecutar pruebas de integración
pytest tests/integration

# Usar script auxiliar (Windows)
run_tests.bat

# Usar script auxiliar (Linux/macOS)
bash run_tests.sh
```

## Uso con Postman

Para probar la API con Postman:

1. Configura una petición POST a `http://localhost:8000/api/v1/convert`
2. En la pestaña "Headers", añade:
   - Key: `X-API-Key`
   - Value: `development_key_change_me` (o el valor que hayas definido en `.env`)
3. En la pestaña "Body", selecciona "form-data" y añade:
   - Key: `image`, Type: File, Value: [Selecciona un archivo de imagen]
   - Key: `format`, Type: Text, Value: `json`
   - Key: `preprocess`, Type: Text, Value: `grayscale,normalize` (opcional)
4. Envía la petición

## Configuración

La configuración se gestiona a través de variables de entorno o el archivo `.env`:

| Variable | Descripción | Valor predeterminado |
|----------|-------------|----------------------|
| API_HOST | Host donde se ejecuta la API | 0.0.0.0 |
| API_PORT | Puerto en el que escucha la API | 8000 |
| DEBUG | Modo de depuración | False |
| LOG_LEVEL | Nivel de registro | INFO |
| MAX_IMAGE_SIZE | Tamaño máximo de imagen (bytes) | 10485760 (10MB) |
| ALLOWED_EXTENSIONS | Extensiones permitidas | jpg,jpeg,png,bmp,tiff |
| API_KEY_HEADER | Nombre de la cabecera para la clave API | X-API-Key |
| DEFAULT_API_KEY | Clave API predeterminada | development_key_change_me |

## Integración como Microservicio

Este proyecto está diseñado para integrarse fácilmente en una arquitectura de microservicios:

- **Stateless**: No mantiene estado entre peticiones, facilitando el escalado horizontal
- **Containerizado**: Incluye configuración para Docker y Docker Compose
- **Health Check**: Proporciona endpoint para verificación de salud (`/health`)
- **Métricas y Logging**: Incluye middleware para registro detallado y métricas
- **Configuración externalizada**: Toda la configuración se puede modificar con variables de entorno

### Ejemplo de integración con Kubernetes

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
        ports:
        - containerPort: 8000
        env:
        - name: DEFAULT_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: api-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Despliegue en producción

Para desplegar este microservicio en un entorno de producción, sigue estas recomendaciones:

### 1. Seguridad

- Cambia la clave API predeterminada (`DEFAULT_API_KEY`)
- Utiliza un proxy inverso como Nginx para SSL/TLS
- Configura los CORS adecuadamente para tus dominios
- Limita los recursos disponibles para el contenedor

### 2. Despliegue en servidor propio

```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
apt-get update && apt-get install -y python3 python3-pip libgl1-mesa-glx libglib2.0-0 curl

# Clonar el repositorio
git clone https://github.com/yourusername/ImageToMatrix.git
cd ImageToMatrix

# Configurar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar según sea necesario

# Ejecutar con gunicorn para producción
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.app:app --bind 0.0.0.0:8000
```

### 3. Despliegue en servicios cloud

#### AWS Elastic Beanstalk

1. Crea un archivo `Procfile` en la raíz:
   ```
   web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.app:app
   ```

2. Despliega con la CLI de EB:
   ```bash
   pip install awsebcli
   eb init
   eb create
   eb deploy
   ```

#### Google Cloud Run

1. Construye y publica la imagen Docker:
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT-ID]/imagetomatrix
   gcloud run deploy --image gcr.io/[PROJECT-ID]/imagetomatrix --platform managed
   ```

#### Heroku

1. Crea un archivo `Procfile` en la raíz:
   ```
   web: uvicorn src.api.app:app --host=0.0.0.0 --port=${PORT:-8000}
   ```

2. Despliega con Git:
   ```bash
   heroku create
   git push heroku main
   ```

## Mantenimiento y escalabilidad

- **Logging**: Revisa los logs regularmente para detectar errores
- **Monitoreo**: Implementa herramientas de monitoreo como Prometheus + Grafana
- **Escalado**: Para aumentar la capacidad, incrementa el número de réplicas en Kubernetes o Docker Swarm
- **Caché**: Implementa caché Redis para mejorar el rendimiento en transformaciones frecuentes

## Solución de problemas comunes

### Error "API key missing"
- Verifica que estás incluyendo el header `X-API-Key` con el valor correcto

### Error al procesar imágenes grandes
- Ajusta `MAX_IMAGE_SIZE` en el archivo `.env`
- Asegúrate de tener suficiente memoria asignada si usas containers

### Problemas con OpenCV
- Instala las dependencias del sistema necesarias: `libgl1-mesa-glx` y `libglib2.0-0`

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

[MIT](LICENSE)
