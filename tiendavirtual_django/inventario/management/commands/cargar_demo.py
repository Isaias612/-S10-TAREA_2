from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventario.models import Categoria, Marca, Producto, Cliente, Perfil

class Command(BaseCommand):
    help = "Carga información de ejemplo para probar el sistema"
    def handle(self, *args, **kwargs):
        for nombre in [
            "Computadoras",
    "Telefonía",
    "Periféricos",
    "Accesorios",
        ]:
            Categoria.objects.get_or_create(nombre=nombre)
        for nombre in [
            "Lenovo",
    "Samsung",
    "Logitech",
        ]:
            Marca.objects.get_or_create(nombre=nombre)
        for nombre, codigo, marca_nombre, precio, stock, categoria_nombre in [
            ('Laptop IdeaPad 3', 'LENOVO01', 'Lenovo', "649.99", 8, 'Computadoras'),
    ('Galaxy A55', 'SAMSUNG01', 'Samsung', "429.00", 12, 'Telefonía'),
    ('Mouse inalámbrico M190', 'LOGI001', 'Logitech', "19.50", 25, 'Periféricos'),
        ]:
            producto, _ = Producto.objects.get_or_create(codigo=codigo, defaults={
                "nombre": nombre, "marca": Marca.objects.get(nombre=marca_nombre),
                "precio": precio, "stock": stock
            })
            producto.categorias.add(Categoria.objects.get(nombre=categoria_nombre))
        for nombres, apellidos, email, telefono, direccion in [
            ('Valeria', 'Mendoza', 'valeria@example.com', '0991234567', 'Milagro'),
    ('Andrés', 'Paredes', 'andres@example.com', '0987654321', 'Guayaquil'),
        ]:
            cedula = str(1000000000 + len(email) * 12345)[:10]
            Cliente.objects.get_or_create(cedula=cedula, defaults={
                "nombres": nombres, "apellidos": apellidos, "email": email,
                "telefono": telefono, "direccion": direccion
            })
        usuario, creado = User.objects.get_or_create(username="admin")
        if creado:
            usuario.set_password("Admin12345!")
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.save()
        Perfil.objects.get_or_create(usuario=usuario)
        self.stdout.write(self.style.SUCCESS("Datos de ejemplo listos. Usuario admin / clave Admin12345!"))
