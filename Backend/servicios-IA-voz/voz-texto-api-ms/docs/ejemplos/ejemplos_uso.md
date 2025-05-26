# Ejemplos de Uso de la API de Voz a Texto

Este documento contiene ejemplos de uso de la API de transcripción de voz a texto.

## Ejemplo de Transcripción con curl

### Transcripción Básica

```bash
curl -X POST "http://localhost:8000/api/v1/transcribir" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@archivo_audio.wav"
```

### Transcripción con Opciones Personalizadas

```bash
curl -X POST "http://localhost:8000/api/v1/transcribir" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "archivo=@archivo_audio.wav" \
  -F 'opciones={"idioma": "es-ES", "modelo": "general"}'
```

## Ejemplo de Verificación de Salud

```bash
curl -X GET "http://localhost:8000/salud" \
  -H "accept: application/json"
```

## Ejemplo de Uso con Python

```python
import requests

def transcribir_audio(ruta_archivo, opciones=None):
    """
    Transcribe un archivo de audio utilizando la API.
    
    Args:
        ruta_archivo: Ruta al archivo de audio
        opciones: Diccionario con opciones adicionales
        
    Returns:
        Texto transcrito
    """
    url = "http://localhost:8000/api/v1/transcribir"
    
    # Crear el objeto multipart/form-data
    files = {"archivo": open(ruta_archivo, "rb")}
    data = {}
    
    # Añadir opciones si se proporcionan
    if opciones:
        import json
        data["opciones"] = json.dumps(opciones)
    
    # Enviar la solicitud
    respuesta = requests.post(url, files=files, data=data)
    
    # Verificar si la respuesta es exitosa
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos["texto"]
    else:
        # Manejar error
        try:
            error = respuesta.json()
            mensaje = error.get("detail", "Error desconocido")
        except:
            mensaje = f"Error {respuesta.status_code}"
        
        raise Exception(f"Error al transcribir audio: {mensaje}")

# Ejemplo de uso
if __name__ == "__main__":
    # Transcripción básica
    texto = transcribir_audio("archivo_audio.wav")
    print(f"Texto transcrito: {texto}")
    
    # Transcripción con opciones
    opciones = {
        "idioma": "es-ES",
        "modelo": "general"
    }
    texto = transcribir_audio("archivo_audio.wav", opciones)
    print(f"Texto transcrito con opciones: {texto}")
```

## Ejemplo de Uso con JavaScript

```javascript
/**
 * Transcribe un archivo de audio utilizando la API.
 * 
 * @param {File} archivo - Archivo de audio a transcribir
 * @param {Object} opciones - Opciones adicionales
 * @returns {Promise<string>} - Texto transcrito
 */
async function transcribirAudio(archivo, opciones = null) {
    const url = 'http://localhost:8000/api/v1/transcribir';
    
    // Crear el objeto FormData
    const formData = new FormData();
    formData.append('archivo', archivo);
    
    // Añadir opciones si se proporcionan
    if (opciones) {
        formData.append('opciones', JSON.stringify(opciones));
    }
    
    try {
        // Enviar la solicitud
        const respuesta = await fetch(url, {
            method: 'POST',
            body: formData
        });
        
        // Verificar si la respuesta es exitosa
        if (!respuesta.ok) {
            const error = await respuesta.json();
            throw new Error(error.detail || 'Error desconocido');
        }
        
        // Procesar la respuesta
        const datos = await respuesta.json();
        return datos.texto;
    } catch (error) {
        console.error('Error al transcribir audio:', error);
        throw error;
    }
}

// Ejemplo de uso
document.getElementById('formulario').addEventListener('submit', async (evento) => {
    evento.preventDefault();
    
    const archivo = document.getElementById('archivo').files[0];
    const idioma = document.getElementById('idioma').value;
    
    try {
        const texto = await transcribirAudio(archivo, { idioma });
        document.getElementById('resultado').textContent = texto;
    } catch (error) {
        document.getElementById('resultado').textContent = `Error: ${error.message}`;
    }
});
```
