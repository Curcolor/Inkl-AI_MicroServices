# Guía de Integración - Servicio de Texto a Voz

> **¡Importante!** Este servicio ha sido actualizado para funcionar principalmente en el navegador del cliente. 
> Por favor, consulte el documento [integracion_cliente.md](integracion_cliente.md) para obtener información
> sobre la nueva arquitectura basada en Web Speech API.

Este documento proporciona información sobre los endpoints anteriores que han sido simplificados.

## Endpoints Actuales

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

## Motivos del Cambio de Arquitectura

El servicio ha sido rediseñado para operar principalmente en el cliente debido a varias ventajas:

1. **Mayor eficiencia**: Elimina la necesidad de transferir archivos de audio entre servidor y cliente
2. **Reducción de carga en el servidor**: El procesamiento ocurre en el dispositivo del usuario
3. **Mayor privacidad**: Los textos no se almacenan ni procesan en el servidor
4. **Funcionamiento offline**: Una vez cargada la interfaz, no se requiere conexión permanente al servidor
5. **Mejor experiencia de usuario**: Respuesta inmediata sin latencia de red

## Recomendaciones para la Migración

Si estaba utilizando la versión anterior de la API, le recomendamos:

1. Migrar a la Web Speech API para nuevas implementaciones
2. Comprobar la compatibilidad de los navegadores objetivo
3. Implementar un mecanismo de fallback para navegadores no compatibles

Para más detalles sobre la implementación cliente, consulte [integracion_cliente.md](integracion_cliente.md).
}
```

### 2. Reproducir Texto Directamente

**Endpoint**: `/api/tts/reproducir`
**Método**: POST
**Descripción**: Reproduce el texto directamente en el servidor donde se está ejecutando el servicio.

#### Solicitud

```json
{
  "texto": "Texto que deseas que se reproduzca como voz",
  "velocidad": 150,                // Opcional (50-300 palabras por minuto)
  "volumen": 1.0,                  // Opcional (0.0-1.0)
  "voz": "HKEY_LOCAL_MACHINE\\..."  // Opcional (ID de voz específica)
}
```

#### Respuesta Exitosa (200 OK)

```json
{
  "estado": "reproducido",
  "texto_longitud": 45,
  "duracion_estimada": 2.25,
  "tiempo_proceso": 0.35,
  "mensaje": "Texto reproducido exitosamente en el servidor"
}
```

#### Respuesta de Error (400 Bad Request)

```json
{
  "mensaje": "Solicitud inválida: El campo 'texto' es obligatorio",
  "codigo": "SOLICITUD_INVALIDA"
}
```

#### Respuesta de Error (500 Internal Server Error)

```json
{
  "mensaje": "Error interno del servidor",
  "codigo": "ERROR_SERVIDOR",
  "detalles": {
    "error_original": "Error al convertir texto a voz"
  }
}
```

### 2. Obtener Voces Disponibles

**Endpoint**: `/api/tts/voces`
**Método**: GET
**Descripción**: Devuelve una lista de las voces disponibles en el sistema.

#### Respuesta Exitosa (200 OK)

```json
{
  "voces": [
    {
      "id": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0",
      "nombre": "Microsoft Helena Desktop - Spanish (Spain)",
      "idiomas": ["es-ES"],
      "genero": "female"
    },
    {
      "id": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0",
      "nombre": "Microsoft David Desktop - English (United States)",
      "idiomas": ["en-US"],
      "genero": "male"
    }
  ],
  "cantidad": 2
}
```

### 3. Estado del Servicio

**Endpoint**: `/api/tts/estado`
**Método**: GET
**Descripción**: Verifica el estado actual del servicio de texto a voz.

#### Respuesta Exitosa (200 OK)

```json
{
  "estado": "operativo",
  "mensaje": "El servicio de texto a voz está funcionando correctamente",
  "max_texto": 1000,
  "timestamp": 1683123456.789
}
```

## Ejemplos de Integración

### Python

```python
import requests
import json

def texto_a_voz(texto, url_base="http://localhost:5002"):
    """
    Envía texto al servicio TTS y devuelve la URL del audio.
    
    Args:
        texto (str): El texto a convertir en voz.
        url_base (str): URL base del servicio.
        
    Returns:
        str: URL del archivo de audio o None si hay error.
    """
    try:
        respuesta = requests.post(
            f"{url_base}/api/tts/convertir",
            json={"texto": texto},
            timeout=30
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()["audio_url"]
        else:
            print(f"Error: {respuesta.status_code}")
            print(json.dumps(respuesta.json(), indent=2))
            return None
            
    except Exception as e:
        print(f"Error al conectar con el servicio: {str(e)}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    url_audio = texto_a_voz("Hola, este es un ejemplo de texto a voz utilizando pyttsx3 en Python.")
    if url_audio:
        print(f"Audio generado disponible en: {url_audio}")

def reproducir_texto_directo(texto, url_base="http://localhost:5002"):
    """
    Envía texto al servicio TTS para reproducirlo directamente en el servidor.
    
    Args:
        texto (str): El texto a reproducir como voz.
        url_base (str): URL base del servicio.
        
    Returns:
        bool: True si se reprodujo correctamente, False en caso contrario.
    """
    try:
        respuesta = requests.post(
            f"{url_base}/api/tts/reproducir",
            json={"texto": texto},
            timeout=30
        )
        
        if respuesta.status_code == 200:
            print("Texto reproducido exitosamente en el servidor")
            return True
        else:
            print(f"Error: {respuesta.status_code}")
            print(json.dumps(respuesta.json(), indent=2))
            return False
            
    except Exception as e:
        print(f"Error al conectar con el servicio: {str(e)}")
        return False

# Ejemplo de uso del método de reproducción directa
if __name__ == "__main__":
    reproducir_texto_directo("Este texto se reproducirá directamente en el servidor.")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

/**
 * Envía texto al servicio TTS y devuelve la URL del audio.
 * 
 * @param {string} texto - El texto a convertir en voz.
 * @param {string} urlBase - URL base del servicio.
 * @returns {Promise<string|null>} - URL del archivo de audio o null si hay error.
 */
async function textoAVoz(texto, urlBase = 'http://localhost:5002') {
  try {
    const respuesta = await axios.post(`${urlBase}/api/tts/convertir`, {
      texto: texto
    }, {
      timeout: 30000
    });
    
    return respuesta.data.audio_url;
    
  } catch (error) {
    console.error('Error al conectar con el servicio:', error.message);
    if (error.response) {
      console.error('Datos de respuesta:', error.response.data);
    }
    return null;
  }
}

/**
 * Envía texto al servicio TTS para reproducirlo directamente en el servidor.
 * 
 * @param {string} texto - El texto a reproducir como voz.
 * @param {string} urlBase - URL base del servicio.
 * @returns {Promise<boolean>} - True si se reprodujo correctamente, false en caso contrario.
 */
async function reproducirTextoDirecto(texto, urlBase = 'http://localhost:5002') {
  try {
    const respuesta = await axios.post(`${urlBase}/api/tts/reproducir`, {
      texto: texto
    }, {
      timeout: 30000
    });
    
    console.log('Texto reproducido exitosamente en el servidor');
    return true;
    
  } catch (error) {
    console.error('Error al conectar con el servicio:', error.message);
    if (error.response) {
      console.error('Datos de respuesta:', error.response.data);
    }
    return false;
  }
}

// Ejemplo de uso
textoAVoz('Hola, este es un ejemplo de texto a voz utilizando pyttsx3 en Python.')
  .then(urlAudio => {
    if (urlAudio) {
      console.log(`Audio generado disponible en: ${urlAudio}`);
    }
  });

// Ejemplo de uso del método de reproducción directa
reproducirTextoDirecto('Este texto se reproducirá directamente en el servidor.')
  .then(resultado => {
    if (resultado) {
      console.log('La reproducción se ha realizado correctamente en el servidor');
    }
  });
```

## Consideraciones de Uso

1. **Límites de Texto**: El servicio tiene un límite de 1000 caracteres por solicitud para evitar sobrecarga.
2. **Persistencia de Archivos**: Los archivos de audio generados se mantienen en el servidor durante una hora (3600 segundos) y luego son eliminados automáticamente.
3. **Concurrencia**: El servicio está diseñado para manejar múltiples solicitudes simultáneas de manera eficiente.
4. **Formatos de Audio**: Actualmente, el servicio genera archivos en formato WAV. Si necesita otros formatos (como MP3), considere convertir el archivo en el cliente.

## Consideraciones de Seguridad

1. **Autenticación**: Esta versión básica no incluye autenticación. En un entorno de producción, se recomienda implementar un mecanismo de autenticación como JWT o API Keys.
2. **Rate Limiting**: Considere implementar limitaciones de tasa para evitar el abuso de la API.
3. **Validación de Entrada**: Aunque la API valida la longitud del texto, es recomendable validar el contenido del texto en su aplicación cliente.
4. **HTTPS**: En producción, siempre use HTTPS para las comunicaciones.
