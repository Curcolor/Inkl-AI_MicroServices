# Ejemplos de Implementación del Servicio TTS

Este directorio contiene ejemplos de cómo utilizar el servicio de conversión de texto a voz de InklúAI.

## Archivos disponibles

1. `ejemplo_tts.js` - Ejemplo de uso con JavaScript (cliente-servidor, versión anterior)
2. `ejemplo_tts.py` - Ejemplo de uso con Python (cliente-servidor, versión anterior)
3. `ejemplo-cliente.js` - Ejemplo actualizado que utiliza la Web Speech API (solo cliente)

## Arquitectura Actualizada

El servicio ha sido rediseñado para funcionar principalmente en el navegador del cliente utilizando la Web Speech API. Las principales ventajas de este enfoque son:

- Mayor eficiencia (sin transferencia de archivos de audio)
- Mejor privacidad (los textos no salen del dispositivo del usuario)
- Funcionamiento sin conexión permanente al servidor
- Respuesta inmediata sin latencia de red

Se recomienda utilizar `ejemplo-cliente.js` para nuevas implementaciones.

## Ejemplo Web Speech API

Para utilizar la Web Speech API:

1. Incluye el archivo `ejemplo-cliente.js` en tu proyecto
2. Utiliza el HTML de ejemplo incluido como comentario al final del archivo
3. Asegúrate de que tus usuarios utilicen navegadores compatibles con la Web Speech API

## Compatibilidad

La Web Speech API es compatible con los siguientes navegadores:

- Chrome 33+
- Edge 79+
- Safari 7+
- Firefox 49+
- Opera 65+

Para navegadores no compatibles, considera implementar un mecanismo de fallback utilizando el servidor.
