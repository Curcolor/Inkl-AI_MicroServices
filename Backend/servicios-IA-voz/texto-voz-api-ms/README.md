# Microservicio de Texto a Voz (Servidor Minimalista)

Este microservicio proporciona un backend minimalista para el sistema de texto a voz que ahora funciona principalmente en el navegador del cliente usando la Web Speech API.

## Nueva Arquitectura

La arquitectura ha sido transformada para operar principalmente en el navegador del cliente:

- **Cliente**: Ejecuta la conversión de texto a voz directamente usando la Web Speech API del navegador
- **Servidor**: Proporciona un backend minimalista que simplemente informa sobre el estado del servicio

## Características Actuales

- Endpoint para verificar el estado del servicio
- Información sobre la arquitectura cliente-servidor
- Configuración minimalista para compatibilidad con el sistema anterior

## Ventajas de la Nueva Arquitectura

1. **Mayor eficiencia**: No es necesario transferir archivos de audio entre el servidor y el cliente
2. **Reducción de carga en el servidor**: El procesamiento ocurre en el dispositivo del usuario
3. **Mayor privacidad**: Los textos no se almacenan ni procesan en el servidor
4. **Funcionamiento offline**: Una vez cargada la interfaz, no se requiere conexión permanente al servidor
5. **Menor complejidad de mantenimiento**: Código más simple y menos puntos de fallo

## Requisitos

- Python 3.7+
- Flask 2.0+
- flask-cors 3.0+
- Bibliotecas adicionales especificadas en `requirements.txt`

## Instalación

1. Clonar el repositorio o descargar los archivos del microservicio.

2. Instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar el servidor con:

```bash
python run.py
```

2. El servidor estará disponible en `http://localhost:5002`

3. Abrir el frontend desde un navegador web compatible con Web Speech API

## Estructura del Proyecto

```
texto-voz-api-ms/
├── app/
│   ├── models/           # Modelos de datos (minimalistas)
│   ├── routes/           # Definición de rutas básicas de la API
│   ├── services/         # Servicios básicos (verificación de estado)
│   ├── static/           # Archivos estáticos (mantenido por compatibilidad)
│   ├── utils/            # Utilidades (manejo de errores, etc.)
│   ├── __init__.py       # Inicialización de la aplicación Flask
│   └── config.py         # Configuración de la aplicación 
├── docs/                 # Documentación
│   └── integracion.md    # Guía de integración de la API
├── requirements.txt      # Dependencias del proyecto
└── run.py                # Punto de entrada del servidor
```

## Endpoints de la API

La API se ha simplificado y ahora ofrece los siguientes endpoints:

- `GET /api/tts/estado` - Comprueba el estado del servicio e informa sobre el modo cliente
- `GET /api/tts/voces` - Proporciona información sobre la obtención de voces mediante Web Speech API

## Transición y Retrocompatibilidad

Este servicio representa una evolución de la arquitectura anterior centrada en el servidor. La nueva implementación:

1. Mantiene las mismas rutas de API para garantizar la compatibilidad
2. Proporciona mensajes informativos que indican al cliente el uso de la Web Speech API
3. Conserva la estructura del proyecto para facilitar el mantenimiento y las actualizaciones futuras

## Consideraciones de Despliegue

Para entornos de producción:
- Considerar el uso de un proxy inverso como Nginx para servir la aplicación
- Configurar correctamente los encabezados CORS para permitir el acceso desde dominios específicos
- Implementar un mecanismo de retrocompatibilidad para navegadores sin soporte para Web Speech API
