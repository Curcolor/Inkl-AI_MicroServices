#!/bin/bash

# Script para configurar el entorno de desarrollo

# Crear entorno virtual
echo "Creando entorno virtual..."
python -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env a partir de .env.example si no existe
if [ ! -f .env ]; then
    echo "Creando archivo .env a partir de .env.example..."
    cp .env.example .env
    echo "Recuerde configurar las variables de entorno en el archivo .env"
else
    echo "El archivo .env ya existe"
fi

# Crear directorios necesarios
echo "Creando directorios necesarios..."
mkdir -p logs

echo "Configuración completada."
echo "Para activar el entorno virtual, ejecute: source venv/bin/activate"
echo "Para iniciar la aplicación, ejecute: python run.py"
