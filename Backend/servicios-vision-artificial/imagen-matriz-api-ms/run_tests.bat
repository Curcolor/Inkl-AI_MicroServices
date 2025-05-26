@echo off
REM Script para ejecutar pruebas con el PYTHONPATH configurado correctamente en Windows

REM Determinar la ruta del directorio raíz del proyecto (donde se encuentra este script)
set "PROJECT_ROOT=%~dp0"
REM Eliminar la barra final en la ruta
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM Agregar el directorio raíz al PYTHONPATH
set "PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%"

REM Mostrar el PYTHONPATH configurado (para depuración)
echo PYTHONPATH: %PYTHONPATH%

REM Ejecutar las pruebas usando pytest
if "%1" == "" (
    REM Sin argumentos, ejecutar todas las pruebas
    python -m pytest
) else (
    REM Ejecutar las pruebas especificadas
    python -m pytest %*
)
