# 🚀 InklúAI MicroServices

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-Enabled-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

**Plataforma de Microservicios de Inteligencia Artificial** que proporciona servicios especializados en procesamiento de voz, texto y visión artificial. Diseñada con arquitectura modular, escalable y containerizada para aplicaciones empresariales.

## 📋 Tabla de Contenidos

- [🔧 Arquitectura del Sistema](#-arquitectura-del-sistema)
- [🎯 Servicios Disponibles](#-servicios-disponibles)
- [⚡ Inicio Rápido](#-inicio-rápido)
- [🛠️ Instalación](#️-instalación)
- [🌐 Configuración](#-configuración)
- [📖 Documentación de APIs](#-documentación-de-apis)
- [🐳 Despliegue con Docker](#-despliegue-con-docker)
- [🧪 Testing](#-testing)
- [🤝 Contribución](#-contribución)
- [📄 Licencia](#-licencia)

## 🔧 Arquitectura del Sistema

InklúAI MicroServices está construido siguiendo los principios de arquitectura de microservicios, proporcionando:

```
InklúAI_MicroServices/
├── Backend/
│   ├── database/                    # Servicios de base de datos
│   ├── gateway/                     # API Gateway principal
│   ├── servicios-IA-voz/           # Servicios de procesamiento de voz
│   │   ├── deepseek-api-ms/        # Procesamiento de texto con IA
│   │   ├── texto-voz-api-ms/       # Conversión texto a voz
│   │   ├── voz-texto-api-ms/       # Conversión voz a texto
│   │   └── voz-flujo-coordinador/  # Coordinador de flujos de voz
│   └── servicios-vision-artificial/ # Servicios de visión artificial
│       ├── imagen-matriz-api-ms/    # Conversión imagen a matriz
│       ├── matriz-imagen-api-ms/    # Conversión matriz a imagen
│       ├── vision-artificial-api-ms/# Análisis de visión artificial
│       └── imagen-flujo-coordinador/# Coordinador de flujos de imagen
├── Frontend/                        # Aplicaciones cliente
├── docs/                           # Documentación del proyecto
└── scripts/                        # Scripts de automatización
```

### 🏗️ Principios de Diseño

- **🔗 Desacoplamiento**: Cada microservicio es independiente y se comunica via APIs REST
- **📈 Escalabilidad**: Servicios stateless que permiten escalado horizontal
- **🛡️ Resiliencia**: Manejo de errores, reintentos automáticos y circuit breakers
- **🔒 Seguridad**: Autenticación por API Keys y validación de entrada
- **📊 Observabilidad**: Logging detallado, health checks y métricas

## 🎯 Servicios Disponibles

### 🎤 Servicios de IA y Voz

#### 🤖 DeepSeek API (Puerto: 5003)
Microservicio para procesamiento de texto con IA utilizando la API de DeepSeek.

**Características:**
- Procesamiento de texto con modelos de lenguaje avanzados
- Soporte para múltiples modelos de DeepSeek
- Configuración de temperatura y tokens
- Manejo de errores y reintentos automáticos

**Endpoints principales:**
- `GET /salud` - Estado del servicio
- `POST /api/v1/ia/procesar` - Procesamiento de texto
- `GET /api/v1/ia/estado` - Estado de DeepSeek

#### 🗣️ Texto a Voz API (Puerto: 5002)
Servicio optimizado que utiliza Web Speech API del navegador para síntesis de voz.

**Características:**
- Arquitectura cliente-servidor optimizada
- Soporte nativo para múltiples idiomas y voces
- Procesamiento en tiempo real sin latencia de red
- Mayor privacidad (texto nunca sale del dispositivo)

**Endpoints principales:**
- `GET /api/tts/estado` - Estado del servicio
- `GET /api/tts/voces` - Información sobre voces disponibles

#### 🎧 Voz a Texto API (Puerto: 8000)
Microservicio para transcripción de audio a texto con soporte para múltiples formatos.

**Características:**
- Soporte para WAV, MP3, OGG, WEBM
- Múltiples motores de transcripción (local, Google, etc.)
- Validación de archivos y optimización de calidad
- Interfaz web para pruebas

**Endpoints principales:**
- `POST /api/v1/transcribir` - Transcripción de audio
- `GET /salud` - Estado del servicio
- `GET /` - Interfaz web de pruebas

### 👁️ Servicios de Visión Artificial

#### 📸 Imagen a Matriz API (Puerto: 8000)
Convierte imágenes en matrices numéricas para procesamiento computacional.

**Características:**
- Soporte para múltiples formatos de imagen
- Opciones de preprocesamiento (redimensionado, normalización)
- Extracción de características avanzadas
- Configuración flexible de salida

**Endpoints principales:**
- `POST /api/v1/convert` - Conversión imagen a matriz
- `GET /health` - Health check
- `GET /web` - Interfaz web de pruebas

#### 🖼️ Matriz a Imagen API (Puerto: 8001)
Genera imágenes a partir de matrices numéricas.

**Características:**
- Conversión de matrices a imágenes PNG/JPEG
- Soporte para diferentes formatos de matriz
- Opciones de renderizado y coloración
- Integración con servicios de visión artificial

**Endpoints principales:**
- `POST /api/v1/generate` - Generación de imagen desde matriz
- `GET /health` - Health check
- `POST /api/v1/verify` - Verificación y procesamiento

## ⚡ Inicio Rápido

### Prerrequisitos

- **Python 3.9+**
- **Docker & Docker Compose** (recomendado)
- **Git**

### 🚀 Ejecución con Docker Compose

```bash
# Clonar el repositorio
git clone <repository-url>
cd InklúAI_MicroServices

# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build
```

### 🔧 Ejecución Individual de Servicios

Cada microservicio puede ejecutarse independientemente:

```bash
# Ejemplo: DeepSeek API
cd Backend/servicios-IA-voz/deepseek-api-ms
pip install -r requirements.txt
cp .env.example .env  # Configurar variables
python run.py

# Ejemplo: Voz a Texto API  
cd Backend/servicios-IA-voz/voz-texto-api-ms
pip install -r requirements.txt
python run.py
```

## 🛠️ Instalación

### Instalación Local Completa

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd InklúAI_MicroServices

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Instalar dependencias por servicio
cd Backend/servicios-IA-voz/deepseek-api-ms
pip install -r requirements.txt

cd ../texto-voz-api-ms
pip install -r requirements.txt

cd ../voz-texto-api-ms
pip install -r requirements.txt

# ... continuar para cada servicio
```

### Dependencias del Sistema

**Para servicios de voz:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Descargar FFmpeg desde https://ffmpeg.org/download.html
```

## 🌐 Configuración

### Variables de Entorno

Cada servicio utiliza variables de entorno para configuración. Ejemplo para DeepSeek API:

```bash
# .env para deepseek-api-ms
API_HOST=0.0.0.0
API_PUERTO=5003
NIVEL_LOG=INFO
DEFAULT_API_KEY=tu_clave_secreta
DEEPSEEK_API_KEY=sk-abcd1234
DEEPSEEK_API_URL=https://api.deepseek.com
DEEPSEEK_MODELO=deepseek-chat
TEMPERATURA_PREDETERMINADA=0.7
MAX_TOKENS_PREDETERMINADO=200
REQUEST_TIMEOUT=30
MAX_REINTENTOS=3
TIEMPO_ENTRE_REINTENTOS=2
```

### Configuración de Puertos

| Servicio | Puerto | Protocolo |
|----------|---------|-----------|
| DeepSeek API | 5003 | HTTP |
| Texto-Voz API | 5002 | HTTP |
| Voz-Texto API | 8000 | HTTP |
| Imagen-Matriz API | 8000 | HTTP |
| Matriz-Imagen API | 8001 | HTTP |

### Configuración de Seguridad

```bash
# Configurar API Keys para cada servicio
DEFAULT_API_KEY=clave_segura_para_este_servicio
API_KEY_HEADER=X-API-Key

# Para servicios externos
DEEPSEEK_API_KEY=tu_clave_deepseek
GOOGLE_CLOUD_API_KEY=tu_clave_google  # Para transcripción
```

## 📖 Documentación de APIs

### Documentación Interactiva

Cada servicio incluye documentación automática:

- **DeepSeek API**: http://localhost:5003/docs
- **Texto-Voz API**: http://localhost:5002/docs  
- **Voz-Texto API**: http://localhost:8000/docs
- **Imagen-Matriz API**: http://localhost:8000/docs
- **Matriz-Imagen API**: http://localhost:8001/docs

### Ejemplos de Uso

#### 🤖 Procesamiento de Texto (DeepSeek)

```bash
curl -X POST "http://localhost:5003/api/v1/ia/procesar" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_api_key" \
  -d '{
    "texto": "Traduce este texto al francés: Hola mundo",
    "temperatura": 0.7,
    "max_tokens": 100
  }'
```

#### 🎧 Transcripción de Audio

```bash
curl -X POST "http://localhost:8000/api/v1/transcribir" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@audio.wav"
```

#### 📸 Conversión Imagen a Matriz

```bash
curl -X POST "http://localhost:8000/api/v1/convert" \
  -H "X-API-Key: development_key_change_me" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@imagen.jpg" \
  -F "preprocess=resize_224x224,normalize"
```

### Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 400 | Error en la solicitud |
| 401 | No autorizado (API Key inválida) |
| 413 | Archivo demasiado grande |
| 422 | Error de validación |
| 500 | Error interno del servidor |

## 🐳 Despliegue con Docker

### Docker Compose Completo

```yaml
version: '3.8'

services:
  deepseek-api:
    build: ./Backend/servicios-IA-voz/deepseek-api-ms
    ports:
      - "5003:5003"
    environment:
      - API_HOST=0.0.0.0
      - API_PUERTO=5003
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    
  voz-texto-api:
    build: ./Backend/servicios-IA-voz/voz-texto-api-ms
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PUERTO=8000
    restart: unless-stopped
    
  # ... más servicios
```

### Configuración de Producción

```bash
# Variables para producción
export ENVIRONMENT=production
export DEBUG=False
export LOG_LEVEL=WARNING

# Ejecutar con configuración de producción
docker-compose -f docker-compose.prod.yml up -d
```

### Health Checks

```bash
# Verificar estado de todos los servicios
curl http://localhost:5003/salud  # DeepSeek API
curl http://localhost:5002/health # Texto-Voz API
curl http://localhost:8000/salud  # Voz-Texto API
curl http://localhost:8000/health # Imagen-Matriz API
curl http://localhost:8001/health # Matriz-Imagen API
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests para un servicio específico
cd Backend/servicios-IA-voz/deepseek-api-ms
python -m pytest tests/ -v

# Tests de integración
python -m pytest tests/integration/ -v

# Tests unitarios
python -m pytest tests/unit/ -v

# Coverage
python -m pytest --cov=src tests/
```

### Tests de Integración

```bash
# Test completo del flujo de voz
cd Backend/servicios-IA-voz/
python -m pytest tests/integration/test_voice_flow.py

# Test completo del flujo de visión
cd Backend/servicios-vision-artificial/
python -m pytest tests/integration/test_vision_flow.py
```

## 🔧 Monitoreo y Observabilidad

### Logs

Los logs se almacenan en el directorio `logs/` de cada servicio:

```bash
# Ver logs en tiempo real
tail -f Backend/servicios-IA-voz/deepseek-api-ms/logs/app.log

# Logs con Docker
docker-compose logs -f deepseek-api
```

### Métricas

Cada servicio expone métricas básicas:

- Tiempo de respuesta promedio
- Número de requests por minuto
- Estado de salud del servicio
- Errores por tipo

### Alertas

Configurar alertas para:
- Servicios caídos
- Tiempo de respuesta alto (>5s)
- Tasa de error alta (>5%)
- Uso de memoria/CPU elevado

## 🚀 Escalabilidad

### Escalado Horizontal

```bash
# Escalar servicio específico
docker-compose up --scale deepseek-api=3

# Con Kubernetes
kubectl scale deployment deepseek-api --replicas=3
```

### Load Balancing

Usar NGINX o un API Gateway para distribuir carga:

```nginx
upstream deepseek_backend {
    server deepseek-api-1:5003;
    server deepseek-api-2:5003;
    server deepseek-api-3:5003;
}
```

## 🔒 Seguridad

### Mejores Prácticas

- ✅ Usar HTTPS en producción
- ✅ Rotar API Keys regularmente
- ✅ Validar todas las entradas
- ✅ Limitar tamaño de archivos
- ✅ Implementar rate limiting
- ✅ Auditar logs regularmente

### Configuración SSL/TLS

```bash
# Con Let's Encrypt
certbot --nginx -d tu-dominio.com

# Configurar en NGINX
ssl_certificate /path/to/cert.pem;
ssl_certificate_key /path/to/key.pem;
```

## 🤝 Contribución

### Proceso de Contribución

1. **Fork** el proyecto
2. **Crear** rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear** Pull Request

### Estándares de Código

- Seguir PEP 8 para Python
- Documentar todas las funciones públicas
- Incluir tests para nuevas funcionalidades
- Actualizar documentación correspondiente

### Estructura de Commits

```
tipo(ámbito): descripción breve

Descripción más detallada del cambio.

Fixes #123
```

Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🛠️ Desarrollo

### Configuración del Entorno de Desarrollo

```bash
# Instalar herramientas de desarrollo
pip install black flake8 pytest pytest-cov

# Pre-commit hooks
pip install pre-commit
pre-commit install

# Formatear código
black src/
flake8 src/
```

### Debugging

```bash
# Modo debug
export DEBUG=True
export LOG_LEVEL=DEBUG

# Con debugger
python -m pdb run.py
```

## 📊 Rendimiento

### Benchmarks Típicos

| Servicio | Latencia Promedio | Throughput |
|----------|------------------|------------|
| DeepSeek API | 1-3s | 100 req/min |
| Voz-Texto | 2-5s | 50 req/min |
| Imagen-Matriz | 0.5-2s | 200 req/min |
| Matriz-Imagen | 0.3-1s | 300 req/min |

### Optimización

- Usar caché para respuestas frecuentes
- Implementar conexión pool para APIs externas
- Optimizar procesamiento de imágenes
- Usar async/await donde sea posible

## 🐛 Solución de Problemas

### Problemas Comunes

**Error de conexión con DeepSeek:**
```bash
# Verificar API Key
curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" https://api.deepseek.com/v1/models
```

**Error de transcripción de audio:**
```bash
# Verificar formato de audio
ffmpeg -i audio.wav
```

**Error de memoria con imágenes grandes:**
```bash
# Redimensionar imagen antes de procesar
convert imagen.jpg -resize 1024x1024 imagen_small.jpg
```

### Logs de Debug

```bash
# Activar logs detallados
export LOG_LEVEL=DEBUG

# Ver logs específicos
grep "ERROR" logs/app.log
grep "DeepSeek" logs/app.log
```

## 📈 Roadmap

### Versión 2.0 (Próxima)

- [ ] 🔧 API Gateway centralizado
- [ ] 📊 Dashboard de monitoreo
- [ ] 🔄 Sistema de colas (Redis/RabbitMQ)
- [ ] 🗄️ Base de datos compartida
- [ ] 🔐 Autenticación JWT
- [ ] 📱 SDK para clientes

### Versión 2.1

- [ ] 🤖 Más modelos de IA
- [ ] 🌍 Soporte multi-idioma
- [ ] 📝 Procesamiento batch
- [ ] 🔍 Búsqueda semántica
- [ ] 📊 Analytics avanzados

## 🏢 Casos de Uso

### Aplicaciones Empresariales

- **Contact Centers**: Transcripción automática de llamadas
- **Educación**: Conversión de contenido texto-audio
- **Análisis de Imagen**: Procesamiento de documentos visuales
- **Chatbots**: Integración con sistemas de IA conversacional

### Integraciones Típicas

```python
# Ejemplo: Pipeline completo de procesamiento
import requests

# 1. Transcribir audio a texto
audio_response = requests.post('http://localhost:8000/api/v1/transcribir', 
                              files={'archivo': open('audio.wav', 'rb')})
texto = audio_response.json()['texto']

# 2. Procesar texto con IA
ia_response = requests.post('http://localhost:5003/api/v1/ia/procesar',
                           json={'texto': f'Resume: {texto}'},
                           headers={'X-API-Key': 'tu_key'})
resumen = ia_response.json()['respuesta']

# 3. Convertir resumen a voz (en cliente con Web Speech API)
```

## 📞 Soporte y Comunidad

### Obtener Ayuda

- 📧 **Email**: support@inkluai.com
- 💬 **Discord**: [InklúAI Community](https://discord.gg/inkluai)
- 📖 **Wiki**: [Documentación Extendida](https://docs.inkluai.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/inkluai/microservices/issues)

### Recursos Adicionales

- [Guías de Integración](./docs/integration/)
- [Ejemplos de Código](./docs/examples/)
- [Best Practices](./docs/best-practices/)
- [Troubleshooting Guide](./docs/troubleshooting/)

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 InklúAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <strong>💡 Construido con ❤️ por el equipo de InklúAI</strong><br>
  <sub>© 2025 InklúAI - Todos los derechos reservados</sub>
</p>

<p align="center">
  <a href="#-tabla-de-contenidos">🔝 Volver al inicio</a>
</p>
