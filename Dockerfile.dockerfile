# Usa la imagen oficial de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido local al contenedor en /app
COPY . /app

# Instala las dependencias si es necesario
RUN pip install -r requirements.txt

# Comando predeterminado para ejecutar tu script cuando se inicie el contenedor
CMD ["python", "SuperMongo2.py", "&&", "python", "updataneo.py","&&", "python", "SuperCassandra.py"]

