# Proyecto de Integración FastAPI con PostgreSQL

Este proyecto demuestra cómo usar FastAPI para interactuar con una base de datos PostgreSQL utilizando contenedores Docker tanto para `pgAdmin` como para `Postgres`. Además, se ha configurado un servicio que se ejecuta automáticamente en WSL2 utilizando systemd para facilitar el proceso de desarrollo.

## Instrucciones de Configuración

### Requisitos Previos
- Docker instalado
- Contenedores de PostgreSQL y pgAdmin corriendo en Docker
- WSL 2 habilitado en tu máquina

### Configuración de Docker y PostgreSQL
1. **Copiar el CSV al contenedor de Docker:**
   Para cargar los datos desde un archivo CSV a PostgreSQL dentro de un contenedor Docker, utiliza el siguiente comando:
   ```bash
   docker cp {ruta_del_csv} {nombre_del_contenedor_postgres}/{nombre_del_csv}
2. **Crear la tabla en PostgreSQL:** Ejecuta el archivo Punto 2.sql, que contiene las instrucciones necesarias para crear la tabla con todas las columnas y tipos de datos que correspondan, además de realizar la operación COPY para cargar los datos del CSV a la tabla creada.

### Dependencias de Python
Asegúrate de que las siguientes librerías estén instaladas, especificadas en el archivo requirements.txt:
- pydantic (para crear los modelos)
- python-dotenv (para cargar las variables del archivo .env)

### Limpieza de Datos
- **Eliminar registros nulos:** El archivo CleanDatabase.sql contiene las instrucciones necesarias para eliminar los registros que tienen datos nulos de la base de datos.

### Configuración del archivo .env
- **Crear archivo .env:** Crea un archivo .env donde configures la URL de la base de datos. Este archivo será utilizado dentro de main.py para establecer la conexión a la base de datos.

### FastAPI y Endpoints
1. **Modelo de base de datos:** En main.py, se crean dos clases que definen un modelo de respuesta de la base de datos usando pydantic. Estas clases modelan la estructura de los datos y cómo se retornarán desde la API.

2. **Conexión a la base de datos:** Se carga el archivo .env y se obtiene la URL de la base de datos. Luego se crea una función que establece la conexión con la base de datos y se gestiona su ciclo de vida, permitiendo abrir la conexión al inicio y cerrarla al final de la ejecución.

3. **Creación de endpoints:** Se implementa un endpoint GET que devuelve, de manera paginada (con un máximo de 100 datos por página), los elementos almacenados en la base de datos.

4. **Ejecutar FastAPI:** Para correr el proyecto FastAPI, asegúrate de tener el entorno virtual activo y, en la terminal dentro del mismo directorio, ejecuta el siguiente comando:

    ```bash
    uvicorn main:app --reload
Luego accede a http://127.0.0.1:8000/docs para utilizar la interfaz de Swagger y probar los endpoints.

### Automatización con Systemd en WSL
1. **Crear servicio para FastAPI:** Crea un archivo llamado fastapi_prueba.service que contiene la configuración necesaria para ejecutar el servidor FastAPI como un servicio de systemd.

2. **Habilitar systemd en WSL:**

- Asegúrate de tener WSL 2 instalado.
- Abre WSL y edita el archivo /etc/wsl.conf:
    ```bash
    sudo nano /etc/wsl.conf
- Añade las siguientes líneas:
    ```ini
    [boot]
    systemd=true
- Desde PowerShell, reinicia WSL:
    ```bash
    wsl --shutdown
- Verifica que systemd esté habilitado ejecutando en WSL:
    ```bash
    systemctl list-units --type=service
3. Configurar y habilitar el servicio:

- Crea el archivo del servicio en /etc/systemd/system/fastapi_prueba.service y añade la configuración.
- Recarga los servicios:
    ```bash
    sudo systemctl daemon-reload
- Inicia el servicio:
    ```bash
    sudo systemctl start fastapi_prueba.service
- Habilita el servicio para que se ejecute automáticamente:
    ```bash
    sudo systemctl enable fastapi_prueba.service
- Verifica el estado del servicio:
    ```bash
    sudo systemctl status fastapi_prueba.service
Si todo está bien, deberías poder acceder a la API desde http://localhost:8000/docs.

### Uso de Docker y FastAPI
- **Iniciar el contenedor Docker:** Asegúrate de tener Docker corriendo con los contenedores necesarios para PostgreSQL y pgAdmin.

- Una vez que el servicio de FastAPI esté en marcha y los contenedores estén corriendo, podrás acceder a los datos desde los endpoints definidos en FastAPI.