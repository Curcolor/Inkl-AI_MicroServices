# MatrixToImagen

Un microservicio complementario para ImageToMatrix que permite convertir matrices numéricas de nuevo a imágenes y verificar la integridad de la transformación imagen-matriz-imagen.

## Descripción

Este microservicio proporciona una API REST para convertir matrices numéricas (generadas por ImageToMatrix) de nuevo a imágenes visualizables. Además, incluye funcionalidades para verificar la integridad de la transformación completa, mostrando una comparación visual entre la imagen original y la reconstruida a partir de la matriz.

## Características

- Conversión de matrices numéricas a imágenes visualizables
- Soporte para formatos de entrada JSON y NumPy serializado
- Soporte para múltiples formatos de imagen de salida (PNG, JPG, etc.)
- Verificación de integridad de la transformación imagen → matriz → imagen
- Generación de visualizaciones comparativas
- Interfaz web simple para pruebas

## Arquitectura

Este proyecto sigue la misma arquitectura en capas del microservicio ImageToMatrix:

```
MatrixToImagen/
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
- Microservicio ImageToMatrix funcionando (para la verificación completa)
- Librerías de sistema para OpenCV (en Linux: libgl1-mesa-glx, libglib2.0-0)

## Instalación

### Método 1: Instalación directa

```bash
# Clonar el repositorio
git clone https://github.com/yourusername/MatrixToImagen.git
cd MatrixToImagen

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno (opcional)
cp .env.example .env
# Editar .env con tus configuraciones
```

## Uso

### Ejecución local

```bash
# Iniciar el servicio
uvicorn src.api.app:app --reload --port 8001
```

### Verificar que el servicio está funcionando

```bash
# Comprueba el estado de salud de la API
curl http://localhost:8001/health

# Deberías ver:
# {"status":"healthy"}
```

## Interfaz Web

Para una experiencia más amigable, puedes acceder a la interfaz web de prueba:

```
http://localhost:8001/web
```

Esta interfaz permite:
- Cargar una imagen
- Aplicar opciones de preprocesamiento
- Ver la comparación visual entre la imagen original y la reconstruida

## Endpoints

La API proporciona los siguientes endpoints:

### GET /health

**Descripción**: Comprueba el estado de la API.

**Ejemplo de uso**:
```bash
curl http://localhost:8001/health
```

**Respuesta exitosa**:
```json
{
  "status": "healthy"
}
```

### POST /api/v1/convert

**Descripción**: Convierte una matriz numérica a una imagen.

**Headers requeridos**:
- `X-API-Key`: Clave de autenticación API (valor predeterminado: `development_key_change_me`)

**Parámetros**:

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| matrix | JSON Body | Datos de la matriz en formato JSON | Sí |
| format | Form | Formato de entrada (`json` o `numpy`) | No (default: `json`) |
| output_format | Form | Formato de salida de la imagen | No (default: `png`) |

**Ejemplo JSON de entrada**:
```json
{
  "matrix": [[[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]], [[0.7, 0.8, 0.9], [0.4, 0.5, 0.6]]],
  "shape": [2, 2, 3],
  "dtype": "float32"
}
```

**Respuesta exitosa**: Imagen en el formato solicitado

### POST /api/v1/verify

**Descripción**: Verifica la transformación completa: imagen → matriz → imagen.

**Headers requeridos**:
- `X-API-Key`: Clave de autenticación API (valor predeterminado: `development_key_change_me`)

**Parámetros form-data**:

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| image | File | Archivo de imagen a procesar | Sí |
| preprocess | Text | Opciones de preprocesamiento separadas por comas | No |

**Opciones de preprocesamiento**:
- `grayscale`: Convierte la imagen a escala de grises
- `normalize`: Normaliza los valores de píxeles (0-1)
- `resize_WxH`: Redimensiona la imagen (ejemplo: `resize_224x224`)

**Respuesta exitosa**: Imagen PNG con la comparación visual entre la imagen original, reconstruida y la diferencia.

### Documentación de la API

Una vez iniciado el servicio, puedes acceder a la documentación interactiva en:

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Integración con ImageToMatrix

Este microservicio está diseñado para trabajar en conjunto con ImageToMatrix. Para usar la funcionalidad de verificación completa:

1. Asegúrate de que ImageToMatrix esté en ejecución (por defecto en el puerto 8000)
2. Configura la URL de ImageToMatrix en las variables de entorno o archivo .env:
   ```
   IMAGE_TO_MATRIX_URL=http://localhost:8000/api/v1/convert
   ```
3. Utiliza el endpoint `/api/v1/verify` o la interfaz web para realizar pruebas completas
