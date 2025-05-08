def carrito_context(request):
    carrito = request.session.get('carrito', {})
    return {
        'carrito_items': sum(item['cantidad'] for item in carrito.values()),
        'carrito_total': sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    }