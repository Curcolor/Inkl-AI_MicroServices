# Guía de Integración - Servicio de Texto a Voz (Modo Cliente)

Este documento proporciona información sobre la arquitectura actualizada del servicio texto-a-voz que ahora opera principalmente en el cliente utilizando la Web Speech API.

## Nueva Arquitectura Cliente-Servidor

La funcionalidad de conversión de texto a voz se ha trasladado al navegador del cliente utilizando la API Web Speech. Esta arquitectura:

1. Elimina la necesidad de procesamiento en el servidor
2. Mejora la privacidad al mantener el texto en el cliente
3. Reduce el consumo de recursos en el servidor
4. Proporciona una experiencia más rápida para el usuario

## Integración en Aplicaciones Web

### Uso de la Web Speech API

Para integrar la funcionalidad de texto a voz en su aplicación web:

```javascript
// Inicializar el sintetizador de voz
const synth = window.speechSynthesis;

// Obtener las voces disponibles
let voices = [];
function loadVoices() {
  voices = synth.getVoices();
  // Ahora puedes mostrar las voces en una interfaz de usuario
}

// En algunos navegadores, las voces se cargan de forma asíncrona
synth.onvoiceschanged = loadVoices;
loadVoices(); // Intentar cargar inmediatamente también

// Función para reproducir texto
function speak(text, voiceIndex, rate = 1, volume = 1) {
  // Crear un nuevo objeto de síntesis de voz
  const utterance = new SpeechSynthesisUtterance(text);
  
  // Configurar propiedades
  utterance.voice = voices[voiceIndex];
  utterance.rate = rate;
  utterance.volume = volume;
  
  // Eventos para controlar el estado
  utterance.onstart = () => console.log('Comenzó la reproducción');
  utterance.onend = () => console.log('Finalizó la reproducción');
  utterance.onerror = (e) => console.error('Error:', e);
  
  // Reproducir
  synth.speak(utterance);
}
```

### Verificación de Compatibilidad

Para garantizar que su aplicación funcione en todos los navegadores:

```javascript
function checkSpeechSupport() {
  if ('speechSynthesis' in window) {
    return true;
  } else {
    console.error('Este navegador no soporta Web Speech API');
    // Implementar fallback o mostrar mensaje al usuario
    return false;
  }
}
```

## Endpoints de API Minimalistas (Servidor)

El servidor ahora proporciona solo endpoints básicos:

### 1. Verificar Estado del Servicio

**Endpoint**: `/api/tts/estado`  
**Método**: GET  
**Descripción**: Comprueba si el servicio está en funcionamiento e informa sobre la arquitectura cliente.

#### Respuesta (200 OK)

```json
{
  "estado": "operativo",
  "mensaje": "El servicio de texto a voz está funcionando correctamente",
  "modo": "cliente",
  "info": "Este servicio ahora opera principalmente en el navegador del cliente",
  "max_texto": 1000,
  "timestamp": 1621234567.89
}
```

### 2. Información sobre Voces

**Endpoint**: `/api/tts/voces`  
**Método**: GET  
**Descripción**: Proporciona información sobre la obtención de voces mediante Web Speech API.

#### Respuesta (200 OK)

```json
{
  "mensaje": "Las voces ahora se obtienen directamente del navegador usando la Web Speech API",
  "info": "Para acceder a las voces use: window.speechSynthesis.getVoices() en el cliente",
  "documentacion": "https://developer.mozilla.org/es/docs/Web/API/Web_Speech_API",
  "timestamp": 1621234567.89
}
```

## Consideraciones de Compatibilidad

- La Web Speech API es compatible con la mayoría de los navegadores modernos, pero no con todos
- Para navegadores sin soporte, considere implementar un mecanismo de fallback que utilice el servidor
- En casos donde la privacidad es crítica, informe a los usuarios que el texto no sale de su dispositivo

## Ventajas de la Arquitectura Cliente

1. **Rendimiento**: Eliminación de la latencia de red y procesamiento del servidor
2. **Escalabilidad**: Mayor capacidad de usuarios concurrentes sin afectar el rendimiento del servidor
3. **Costos**: Reducción en recursos de servidor necesarios
4. **Privacidad**: Los textos nunca salen del dispositivo del usuario
5. **Experiencia de usuario**: Respuesta inmediata, incluso sin conexión permanente

## Recursos Adicionales

- [Documentación de Web Speech API (MDN)](https://developer.mozilla.org/es/docs/Web/API/Web_Speech_API)
- [Ejemplos de implementación](https://github.com/mdn/web-speech-api)
- [Tabla de compatibilidad de navegadores](https://caniuse.com/speech-synthesis)
