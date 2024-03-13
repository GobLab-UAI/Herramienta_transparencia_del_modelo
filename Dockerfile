# Usar una imagen base oficial de Python
FROM python:3.8-slim

# Instalar dependencias del sistema requeridas por WeasyPrint
RUN apt-get update && apt-get install -y libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos primero para aprovechar la cache de Docker
COPY requirements.txt ./ 

# Instalar las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de tu aplicación en el contenedor
COPY . .

# Exponer el puerto en el que se ejecuta Streamlit
EXPOSE 8501

# Ejecutar la aplicación Streamlit al iniciar el contenedor
CMD ["streamlit", "run", "home.py"]
