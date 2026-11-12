# NovaTech — Django

Aplicación académica de gestión comercial con:
- CRUD de categorías, marcas, productos y clientes.
- Búsqueda de registros.
- Paginación de productos y clientes.
- Inicio de sesión y registro de usuarios.
- Sección Mi perfil.
- Modelos con relaciones ForeignKey, ManyToManyField y OneToOneField.
- Panel de administración de Django.

## Instalación en Windows / PowerShell

Abre la terminal en esta carpeta y ejecuta:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py cargar_demo
python manage.py runserver
```

Abre http://127.0.0.1:8000/

Usuario de demostración: `admin`
Contraseña: `Admin12345!`

También puedes crear tu propio usuario desde Registro.
Cambia la contraseña de demostración antes de publicar el proyecto.
