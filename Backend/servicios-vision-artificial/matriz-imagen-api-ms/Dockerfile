FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Puerto en el que se ejecuta la aplicación
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8001"]
