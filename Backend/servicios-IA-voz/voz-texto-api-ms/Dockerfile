FROM python:3.9-slim

WORKDIR /app

# Instalación de dependencias de sistema para procesamiento de audio
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libportaudio2 \
    portaudio19-dev \
    python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto (se configurará mediante variables de entorno)
# El puerto real se establecerá al ejecutar el contenedor
EXPOSE 8000

# Configurar healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${API_PUERTO}/salud || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "${API_PUERTO}"]
