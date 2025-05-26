@echo off
REM Script para construir y ejecutar el servicio con Docker en Windows

echo Construyendo la imagen Docker...
docker build -t imagetomatrix .

echo Ejecutando el contenedor...
docker run -p 8000:8000 --name imagetomatrix-service imagetomatrix

REM Para detener el contenedor: docker stop imagetomatrix-service
REM Para eliminar el contenedor: docker rm imagetomatrix-service
