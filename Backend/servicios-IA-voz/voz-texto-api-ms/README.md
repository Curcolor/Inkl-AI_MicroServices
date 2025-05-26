# Microservicio de Voz a Texto (voz-texto-api-ms)

Este microservicio proporciona una API para la transcripción de voz a texto utilizando diversos motores de reconocimiento de voz.

## Características

- Transcripción de archivos de audio a texto
- Soporte para múltiples motores de transcripción (local, Google, etc.)
- Validación de archivos de audio (formato, tamaño)
- Interfaz de usuario simple para pruebas
- Documentación completa de la API con Swagger UI

## Requisitos

- Python 3.9+
- FFmpeg (para procesamiento de audio)
- Dependencias de Python listadas en `requirements.txt`

## Configuración

El microservicio se configura mediante variables de entorno. Copia el archivo `.env.example` a `.env` y configura las variables según tus necesidades:

```bash
cp .env.example .env
```

### Variables de entorno requeridas

- `MOTOR_TRANSCRIPCION`: Motor de transcripción a utilizar (local, google, etc.)
- `API_CLAVE`: Clave API para servicios de transcripción externos
- `API_HOST`: Host donde se ejecutará la API
- `API_PUERTO`: Puerto donde se ejecutará la API
- `NIVEL_LOG`: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `TAMANO_MAX_ARCHIVO`: Tamaño máximo permitido para archivos de audio (en MB)
- `FORMATOS_PERMITIDOS`: Lista de formatos de audio permitidos (separados por comas)
- `TIEMPO_ESPERA`: Tiempo máximo de espera para la transcripción (en segundos)

## Instalación y ejecución

### Instalación local

1. Clonar el repositorio
2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar las variables de entorno (ver sección de Configuración)
4. Ejecutar la aplicación:

```bash
python run.py
```

### Ejecución con Docker

1. Construir y ejecutar con Docker Compose:

```bash
docker-compose up --build
```

## Uso de la API

### Endpoints disponibles

- `POST /api/v1/transcribir`: Transcribir un archivo de audio a texto
- `GET /salud`: Verificar el estado del servicio
- `GET /`: Interfaz web para probar la funcionalidad

### Ejemplos de uso

#### Transcribir audio con curl

```bash
curl -X POST "http://localhost:8000/api/v1/transcribir" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@archivo_audio.wav"
```

## Formatos de audio soportados

- WAV
- MP3
- OGG
- WEBM
- Otros formatos configurados en FORMATOS_PERMITIDOS

## Recomendaciones para mejorar la calidad de las transcripciones

- Utilizar audio con buena calidad y sin ruido de fondo
- Hablar de manera clara y a un ritmo normal
- Para audios largos, considerar segmentarlos en partes más pequeñas
- Experimentar con diferentes motores de transcripción según el caso de uso

## Documentación adicional

Para más información, consultar los documentos en la carpeta `docs/`.
