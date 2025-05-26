FROM python:3.10-slim

LABEL maintainer="InklúAI Team <info@inkluai.com>"
LABEL description="Microservicio de texto a voz utilizando Web Speech API"

# Instalar herramientas necesarias para el healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p static/audio
RUN mkdir -p logs

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV API_PORT=5002

# Puerto que expondrá el contenedor
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "5002"]
