"""
Configuración para la instalación del paquete ImageToMatrix.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="imagetomatrix",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu.email@example.com",
    description="API para convertir imágenes a matrices para su procesamiento",
    long_description=long_description,
    long_description_content_type="text/markdown",    url="https://github.com/yourusername/ImageToMatrix",
    packages=find_packages() + ['src', 'src.api', 'src.services', 'src.utils', 'src.config'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "imagetomatrix=src.api.app:main",
        ],
    },
)
