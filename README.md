# backend_store
# Proyecto Django: Configuración y Ejecución

Este proyecto Django requiere la configuración inicial del entorno virtual, instalación de dependencias y configuración de la base de datos. Sigue los pasos a continuación para poner en marcha el proyecto.

# 1. Crear un entorno virtual y activarlo
```bash
python -m venv env
source env/bin/activate  # En Linux/MacOS
env\Scripts\activate     # En Windows
```
# 2. Instalar las dependencias del proyecto
```bash
pip install -r requirements.txt
```
# 3. Crear migraciones para sincronizar los modelos con la base de datos
```bash
python manage.py makemigrations
```
# 4. Aplicar las migraciones a la base de datos
```bash
python manage.py migrate
```
# 5. Crear un superusuario para el panel de administración
```bash
python manage.py createsuperuser
```
# 6. Ejecutar el servidor de desarrollo con detalles adicionales en los logs
```bash
python manage.py runserver --verbosity 3
```

# 7. Verificar el Endpoint de Token
# Abre el archivo requests.ipynb, busca las variables username y password, y cámbialas
# por las credenciales del superusuario creado en el paso 5.
# Luego, ejecuta las celdas para solicitar un token y verificar que el endpoint de autenticación esté funcionando.
