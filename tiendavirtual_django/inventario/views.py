from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Marca, Producto, Cliente, Perfil
from .forms import CategoriaForm, MarcaForm, ProductoForm, ClienteForm, PerfilForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user)
            from django.contrib.auth import login
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/registro.html", {"form": form})

@login_required
def salir(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "total_productos": Producto.objects.count(),
        "total_categorias": Categoria.objects.count(),
        "total_clientes": Cliente.objects.count(),
        "total_marcas": Marca.objects.count(),
    })

def lista_generica(request, modelo, titulo, campos, plantilla):
    q = request.GET.get("q", "").strip()
    datos = modelo.objects.all()
    if q:
        filtro = Q()
        for campo in campos:
            filtro |= Q(**{campo + "__icontains": q})
        datos = datos.filter(filtro)
    return render(request, plantilla, {"registros": datos, "titulo": titulo, "q": q})

@login_required
def categoria_lista(request):
    return lista_generica(request, Categoria, "Categorías", ["nombre", "descripcion"], "catalogos/lista.html")

@login_required
def marca_lista(request):
    return lista_generica(request, Marca, "Marcas", ["nombre", "pais_origen"], "catalogos/lista.html")

def guardar(request, modelo, formulario, titulo, url_lista, pk=None):
    objeto = get_object_or_404(modelo, pk=pk) if pk else None
    form = formulario(request.POST or None, instance=objeto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Registro guardado correctamente.")
        return redirect(url_lista)
    return render(request, "catalogos/formulario.html", {"form": form, "titulo": titulo})

@login_required
def categoria_crear(request): return guardar(request, Categoria, CategoriaForm, "Nueva categoría", "categoria_lista")
@login_required
def categoria_editar(request, pk): return guardar(request, Categoria, CategoriaForm, "Editar categoría", "categoria_lista", pk)
@login_required
def marca_crear(request): return guardar(request, Marca, MarcaForm, "Nueva marca", "marca_lista")
@login_required
def marca_editar(request, pk): return guardar(request, Marca, MarcaForm, "Editar marca", "marca_lista", pk)

@login_required
def eliminar(request, modelo, pk, url_lista):
    objeto = get_object_or_404(modelo, pk=pk)
    if request.method == "POST":
        objeto.delete()
        messages.success(request, "Registro eliminado.")
        return redirect(url_lista)
    return render(request, "catalogos/confirmar.html", {"objeto": objeto})

@login_required
def categoria_eliminar(request, pk): return eliminar(request, Categoria, pk, "categoria_lista")
@login_required
def marca_eliminar(request, pk): return eliminar(request, Marca, pk, "marca_lista")
@login_required
def producto_eliminar(request, pk): return eliminar(request, Producto, pk, "producto_lista")
@login_required
def cliente_eliminar(request, pk): return eliminar(request, Cliente, pk, "cliente_lista")

@login_required
def producto_lista(request):
    q = request.GET.get("q", "").strip()
    datos = Producto.objects.select_related("marca").prefetch_related("categorias")
    if q:
        datos = datos.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q) | Q(marca__nombre__icontains=q))
    pagina = Paginator(datos, 8).get_page(request.GET.get("page"))
    return render(request, "productos/lista.html", {"pagina": pagina, "q": q})

@login_required
def producto_crear(request): return guardar(request, Producto, ProductoForm, "Nuevo producto", "producto_lista")
@login_required
def producto_editar(request, pk): return guardar(request, Producto, ProductoForm, "Editar producto", "producto_lista", pk)

@login_required
def cliente_lista(request):
    q = request.GET.get("q", "").strip()
    datos = Cliente.objects.all()
    if q:
        datos = datos.filter(Q(cedula__icontains=q) | Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(email__icontains=q))
    pagina = Paginator(datos, 8).get_page(request.GET.get("page"))
    return render(request, "clientes/lista.html", {"pagina": pagina, "q": q})

@login_required
def cliente_crear(request): return guardar(request, Cliente, ClienteForm, "Nuevo cliente", "cliente_lista")
@login_required
def cliente_editar(request, pk): return guardar(request, Cliente, ClienteForm, "Editar cliente", "cliente_lista", pk)

@login_required
def mi_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    form = PerfilForm(request.POST or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Perfil actualizado.")
        return redirect("mi_perfil")
    return render(request, "perfil.html", {"form": form})
