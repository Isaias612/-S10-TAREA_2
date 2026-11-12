from django import forms
from .models import Categoria, Marca, Producto, Cliente, Perfil

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "activa"]

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre", "pais_origen", "activa"]

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "codigo", "marca", "categorias", "precio", "stock", "activo"]
        widgets = {"categorias": forms.CheckboxSelectMultiple()}

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos", "email", "telefono", "direccion"]
    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"].strip()
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError("La cédula debe contener exactamente 10 dígitos.")
        return cedula

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["cedula", "telefono", "direccion", "cargo"]
