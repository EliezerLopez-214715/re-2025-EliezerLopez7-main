from django.urls import path
from .import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('telas',views.telas, name='telas'),
    path('merceria',views.merceria, name='merceria'),
    path('accesorios',views.accesorios, name='accesorios'),
    path('decoracion',views.decoracion, name='decoracion'),
    path('hogar',views.hogar, name='hogar'),
    
    path('productmerceria',views.productmerceria, name='productmerceria'),
    path('productmerceria/crear',views.crear, name='crear'),
    path('productmerceria/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('productmerceria/editar/<int:id>', views.editar, name='editar'),

      # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),

    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),

    path('checkout/', views.checkout, name='checkout'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
