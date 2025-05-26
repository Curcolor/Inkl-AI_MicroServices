# Guía de Uso: Verificación de Transformaciones Imagen-Matriz-Imagen

Este documento explica cómo utilizar los microservicios ImageToMatrix y MatrixToImagen para verificar la integridad de las transformaciones de imágenes a matrices numéricas y viceversa.

## Requisitos Previos

1. Python 3.8 o superior
2. Los microservicios ImageToMatrix y MatrixToImagen instalados
3. Dependencias instaladas (`pip install -r requirements.txt` en ambos proyectos)

## Iniciar los Servicios

### 1. Iniciar ImageToMatrix

```bash
# En la carpeta de ImageToMatrix
cd C:\Users\SemilleroTI\Desktop\Workspace\ImageToMatrix
python -m uvicorn src.api.app:app --reload --port 8000
```

### 2. Iniciar MatrixToImagen

```bash
# En la carpeta de MatrixToImagen
cd C:\Users\SemilleroTI\Desktop\Workspace\MatrixToImagen
python -m uvicorn src.api.app:app --reload --port 8001
```

O simplemente ejecute:

```bash
cd C:\Users\SemilleroTI\Desktop\Workspace\MatrixToImagen
run_app.bat
```

## Usando la Interfaz Web

1. **Abrir la interfaz web**:
   - Navegue a http://localhost:8001/web en su navegador
   - O ejecute el script `open_web_ui.py` para abrir automáticamente la interfaz:
   ```bash
   python open_web_ui.py
   ```

2. **Cargar una imagen**:
   - Haga clic en "Seleccione una imagen"
   - Elija cualquier imagen de su computadora (formatos admitidos: JPG, PNG, BMP, TIFF)

3. **Seleccionar opciones de preprocesamiento** (opcional):
   - Escala de grises: Convierte la imagen a escala de grises
   - Normalización: Normaliza los valores de píxeles a un rango de 0-1
   - Redimensionar: Cambia el tamaño de la imagen a las dimensiones especificadas

4. **Verificar la transformación**:
   - Haga clic en el botón "Verificar Transformación"
   - Espere a que se complete el proceso (puede tardar unos segundos)

5. **Interpretar los resultados**:
   - Se mostrará una imagen con tres paneles:
     - **Izquierda**: Imagen original
     - **Centro**: Imagen reconstruida después de la transformación a matriz y de vuelta
     - **Derecha**: Visualización de la diferencia entre ambas imágenes (más brillo = mayor diferencia)

## Interpretación de la Visualización de Diferencias

- **Áreas oscuras**: Indican poca o ninguna diferencia entre la imagen original y la reconstruida
- **Áreas brillantes**: Indican diferencias significativas en esos píxeles
- **Colores**: En imágenes a color, los colores en la visualización de diferencias indican qué canales (R, G, B) tienen más diferencias

## Uso Programático

También puede utilizar los endpoints de la API directamente:

### 1. Verificar transformación imagen-matriz-imagen

```python
import requests

# Preparar la solicitud
url = "http://localhost:8001/api/v1/verify"
api_key = "development_key_change_me"  # Clave API predeterminada

# Con archivo de imagen
with open("ruta/a/imagen.jpg", "rb") as img_file:
    files = {"image": ("imagen.jpg", img_file, "image/jpeg")}
    headers = {"X-API-Key": api_key}
    
    # Agregar preprocesamiento (opcional)
    data = {"preprocess": "grayscale,normalize"}
    
    # Realizar solicitud
    response = requests.post(url, files=files, headers=headers, data=data)
    
    # Guardar resultado
    if response.status_code == 200:
        with open("comparacion.png", "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.text}")
```

## Solución de Problemas

1. **Servicios no disponibles**:
   - Verifique que ambos servicios estén en ejecución (puertos 8000 y 8001)
   - Compruebe los endpoints de salud: http://localhost:8000/health y http://localhost:8001/health

2. **Error de API Key**:
   - Asegúrese de usar la clave API correcta (predeterminada: `development_key_change_me`)
   - Puede configurarla en el archivo `.env` de cada proyecto

3. **Imagen demasiado grande**:
   - Por defecto, hay un límite de 10MB para las imágenes
   - Ajuste `MAX_IMAGE_SIZE` en `settings.py` si necesita trabajar con imágenes más grandes

## Personalización

Para personalizar los servicios, puede modificar:

- **Opciones de preprocesamiento**: Edite `src/services/image_service.py` en ImageToMatrix
- **Visualización de diferencias**: Edite `src/services/matrix_service.py` en MatrixToImagen
- **Interfaz web**: Modifique `src/utils/web_ui.py` en MatrixToImagen
