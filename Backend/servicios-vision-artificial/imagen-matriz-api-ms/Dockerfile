FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias para OpenCV, Pillow y monitorización
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pydantic-settings

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto usado por la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
