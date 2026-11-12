from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Categorías"
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=70, unique=True)
    pais_origen = models.CharField(max_length=60, blank=True)
    activa = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=25, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.apellidos} {self.nombres}"

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    cedula = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    cargo = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return f"Perfil de {self.usuario.username}"
