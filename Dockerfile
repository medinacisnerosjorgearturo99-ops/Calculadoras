# Usamos una imagen oficial y ligera de Python
FROM python:3.11-slim

# Evita que Python escriba archivos .pyc y fuerza que la salida estándar vaya directo a la terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creamos un directorio de trabajo
WORKDIR /app

# Copiamos solo los requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del proyecto
COPY . .

# Exponemos el puerto que usará el contenedor
EXPOSE 5000

# Arrancamos la app usando Gunicorn en lugar del servidor de desarrollo de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]