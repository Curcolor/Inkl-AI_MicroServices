"""
Utilidades para la interfaz web simple.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

def setup_web_ui(app: FastAPI):
    """
    Configura una interfaz web simple para interactuar con la API.
    
    Args:
        app: Aplicación FastAPI
    """
    # Definir las plantillas HTML en línea ya que son muy sencillas
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MatrixToImagen Demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
        <style>
            .result-container {
                max-width: 100%;
                overflow-x: auto;
            }
            .result-image {
                max-width: 100%;
                height: auto;
            }
        </style>
    </head>
    <body>
        <div class="container my-5">
            <h1 class="text-center mb-4">Verificación de Transformación Imagen-Matriz-Imagen</h1>
            
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            Cargar Imagen para Verificación
                        </div>
                        <div class="card-body">
                            <form id="uploadForm" enctype="multipart/form-data" class="mb-4">
                                <div class="mb-3">
                                    <label for="imageFile" class="form-label">Seleccione una imagen:</label>
                                    <input type="file" class="form-control" id="imageFile" name="image" accept="image/*" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label for="preprocess" class="form-label">Opciones de preprocesamiento:</label>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="grayscale" id="grayscaleCheck">
                                        <label class="form-check-label" for="grayscaleCheck">
                                            Escala de grises
                                        </label>
                                    </div>
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" value="normalize" id="normalizeCheck">
                                        <label class="form-check-label" for="normalizeCheck">
                                            Normalizar (0-1)
                                        </label>
                                    </div>
                                    <div class="input-group mt-2">
                                        <span class="input-group-text">Redimensionar</span>
                                        <input type="number" class="form-control" id="resizeWidth" placeholder="Ancho" min="1">
                                        <span class="input-group-text">x</span>
                                        <input type="number" class="form-control" id="resizeHeight" placeholder="Alto" min="1">
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <label for="apiKey" class="form-label">Clave API:</label>
                                    <input type="text" class="form-control" id="apiKey" 
                                           value="development_key_change_me"
                                           placeholder="Ingrese su clave API">
                                    <div class="form-text">Clave por defecto: development_key_change_me</div>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary">Verificar Transformación</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4 justify-content-center d-none" id="resultSection">
                <div class="col-md-10">
                    <div class="card">
                        <div class="card-header bg-success text-white">
                            Resultado de la Verificación
                        </div>
                        <div class="card-body text-center result-container">
                            <div class="spinner-border text-primary d-none" id="loadingSpinner" role="status">
                                <span class="visually-hidden">Cargando...</span>
                            </div>
                            <img id="resultImage" class="result-image" src="" alt="Comparación de imágenes">
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4 justify-content-center">
                <div class="col-md-8">
                    <div class="alert alert-info">
                        <h5>Información:</h5>
                        <p>Esta herramienta verifica la integridad de la conversión imagen-matriz-imagen:</p>
                        <ol>
                            <li>Convierte la imagen original a una matriz numérica utilizando el servicio ImageToMatrix</li>
                            <li>Reconstruye la imagen a partir de la matriz numérica</li>
                            <li>Genera una comparación visual entre la imagen original y la reconstruida</li>
                        </ol>
                        <p>La diferencia absoluta muestra qué tanto se perdió en la transformación.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async function(event) {
                event.preventDefault();
                
                // Mostrar spinner y sección de resultados
                document.getElementById('loadingSpinner').classList.remove('d-none');
                document.getElementById('resultSection').classList.remove('d-none');
                document.getElementById('resultImage').classList.add('d-none');
                
                // Recopilar opciones de preprocesamiento
                const preprocessOptions = [];
                if (document.getElementById('grayscaleCheck').checked) {
                    preprocessOptions.push('grayscale');
                }
                if (document.getElementById('normalizeCheck').checked) {
                    preprocessOptions.push('normalize');
                }
                
                const width = document.getElementById('resizeWidth').value;
                const height = document.getElementById('resizeHeight').value;
                if (width && height) {
                    preprocessOptions.push(`resize_${width}x${height}`);
                }
                
                // Preparar datos del formulario
                const formData = new FormData();
                formData.append('image', document.getElementById('imageFile').files[0]);
                if (preprocessOptions.length > 0) {
                    formData.append('preprocess', preprocessOptions.join(','));
                }
                
                // Obtener API key
                const apiKey = document.getElementById('apiKey').value || 'development_key_change_me';
                
                try {
                    // Realizar solicitud al endpoint de verificación
                    const response = await fetch('/api/v1/verify', {
                        method: 'POST',
                        headers: {
                            'X-API-Key': apiKey
                        },
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error(`Error ${response.status}: ${response.statusText}`);
                    }
                    
                    // Convertir la respuesta a blob para mostrar la imagen
                    const blob = await response.blob();
                    const imageUrl = URL.createObjectURL(blob);
                    
                    // Mostrar la imagen de resultado
                    document.getElementById('resultImage').src = imageUrl;
                    document.getElementById('resultImage').classList.remove('d-none');
                } catch (error) {
                    console.error('Error:', error);
                    alert(`Error al procesar la solicitud: ${error.message}`);
                } finally {
                    // Ocultar spinner
                    document.getElementById('loadingSpinner').classList.add('d-none');
                }
            });
        </script>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    # Agregar ruta para la interfaz web
    @app.get("/web", response_class=HTMLResponse, tags=["Web UI"])
    async def web_ui():
        """Interfaz web simple para interactuar con la API."""
        return html_content
