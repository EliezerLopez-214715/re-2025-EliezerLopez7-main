from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Producto
from .forms import ProductoForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def telas(request):
    telas = Producto.objects.filter(categoria='TELAS')
    return render(request, 'paginas/telas.html', {'telas': telas})
def merceria(request):
    merceria = Producto.objects.filter(categoria='MERCERIA')
    return render(request, 'paginas/merceria.html', {'merceria': merceria})
def accesorios(request):
    accesorios = Producto.objects.filter(categoria='ACCESORIOS')
    return render(request, 'paginas/accesorios.html', {'accesorios': accesorios})
def decoracion(request):
    decoracion = Producto.objects.filter(categoria='DECORACION')
    return render(request, 'paginas/decoracion.html', {'decoracion': decoracion})
def hogar(request):
    hogar = Producto.objects.filter(categoria='HOGAR')
    return render(request, 'paginas/hogar.html', {'hogar': hogar})

def productmerceria(request):
    categoria = request.GET.get('categoria')
    if categoria:
        productmerceria = Producto.objects.filter(categoria__iexact=categoria)
    else:
        productmerceria = Producto.objects.all()
    return render(request, 'productmerceria/index.html', {'productmerceria': productmerceria})

@staff_member_required
def crear(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('productmerceria')
    return render(request,'productmerceria/crear.html',{'formulario': formulario})

@staff_member_required
def editar(request, id):
    producto = Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('productmerceria')
    return render(request,'productmerceria/editar.html', {'formulario': formulario})

@staff_member_required
def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('productmerceria')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido {username}!")
                return redirect('inicio')
        messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso!")
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('inicio')

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verificar stock disponible
    if producto.stock < 1:
        messages.error(request, "Este producto está agotado")
        return redirect(request.META.get('HTTP_REFERER', 'inicio'))
    
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
    
    if producto_id_str in carrito:
        # Verificar que no exceda el stock al agregar más
        if carrito[producto_id_str]['cantidad'] >= producto.stock:
            messages.warning(request, "No hay suficiente stock disponible")
            return redirect(request.META.get('HTTP_REFERER', 'inicio'))
        carrito[producto_id_str]['cantidad'] += 1
    else:
        carrito[producto_id_str] = {
            'cantidad': 1,
            'precio': str(producto.precio),
            'nombre': producto.nombre,
            'imagen': producto.imagen.url if producto.imagen else ''
        }
    
    request.session['carrito'] = carrito
    messages.success(request, f"¡{producto.nombre} agregado al carrito!")
    return redirect(request.META.get('HTTP_REFERER', 'inicio'))

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    
    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * item['cantidad']
        productos.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'subtotal': subtotal
        })
        total += subtotal
    
    return render(request, 'carrito/ver_carrito.html', {
        'productos': productos,
        'total': total
    })

@login_required
def actualizar_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        
        if str(producto_id) in carrito:
            if cantidad > 0:
                carrito[str(producto_id)]['cantidad'] = cantidad
            else:
                del carrito[str(producto_id)]
            request.session['carrito'] = carrito
            request.session['carrito_items'] = len(carrito)    
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session['carrito_items'] = len(carrito)    
    return redirect('ver_carrito')

@login_required
def checkout(request):
    if 'carrito' not in request.session or not request.session['carrito']:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')
    
    carrito = request.session['carrito']
    
    # Verificar stock antes de procesar
    for producto_id, item in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        if producto.stock < item['cantidad']:
            messages.error(request, f"No hay suficiente stock de {producto.nombre}")
            return redirect('ver_carrito')
    
    # Simular proceso de pago
    return render(request, 'carrito/checkout.html', {
        'total': sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    })

@login_required
def procesar_pago(request):
    if 'carrito' not in request.session:
        return redirect('inicio')
    
    carrito = request.session['carrito']
    
    try:
        # Actualizar stock en la base de datos
        for producto_id, item in carrito.items():
            producto = Producto.objects.get(id=producto_id)
            producto.stock -= item['cantidad']
            producto.save()
        
        # Limpiar carrito
        del request.session['carrito']
        del request.session['carrito_items']
        
        messages.success(request, "¡Compra realizada con éxito!")
        return render(request, 'carrito/confirmacion.html')
    
    except Exception as e:
        messages.error(request, f"Error al procesar el pago: {str(e)}")
        return redirect('ver_carrito')


def buscar_productos(request):
    query = request.GET.get('q', '').strip()  # Limpia espacios en blanco
    
    if query:
        # Búsqueda que incluye nombre, descripción y categoría (insensible a mayúsculas)
        resultados = Producto.objects.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(categoria__icontains=query)
        ).distinct()
        
        # Debug (opcional - quitar en producción)
        print(f"Búsqueda: '{query}'")
        print(f"Resultados: {resultados}")
    else:
        resultados = Producto.objects.none()
    
    return render(request, 'productos/busqueda.html', {
        'resultados': resultados,
        'query': query
    })
