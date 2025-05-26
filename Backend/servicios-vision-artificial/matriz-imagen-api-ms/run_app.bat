@echo off
echo Iniciando MatrixToImagen API...

rem Activar entorno virtual si existe
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)

rem Ejecutar la aplicación
python -m uvicorn src.api.app:app --reload --port 8001

rem Si hay un error, pausar para ver el mensaje
if %ERRORLEVEL% neq 0 (
    echo Error al iniciar la aplicación.
    pause
)
