#!/bin/bash

# Script para ejecutar pruebas con el PYTHONPATH configurado correctamente

# Determinar la ruta del directorio raíz del proyecto (donde se encuentra este script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Agregar el directorio raíz al PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH}"

# Mostrar el PYTHONPATH configurado (para depuración)
echo "PYTHONPATH: ${PYTHONPATH}"

# Ejecutar las pruebas usando pytest
if [ $# -eq 0 ]; then
    # Sin argumentos, ejecutar todas las pruebas
    python -m pytest
else
    # Ejecutar las pruebas especificadas
    python -m pytest "$@"
fi
