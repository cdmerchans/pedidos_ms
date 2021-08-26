"""pedidosProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pedidosApp import views
from pedidosApp.views import AgregarProductoCarrito, ConsultarCarrito, ComprarVenta, EliminarProductoCarrito, ConsultarCarritoCliente, ConsultarCarritoActualCliente
from pedidosApp.views import CancelarCompra
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('detalleorder/agregar/', AgregarProductoCarrito.as_view()),
    path('detalleorder/consultar/', ConsultarCarrito.as_view()),
    path('order/comprar/', ComprarVenta.as_view()),
    path('detalleorder/eliminar', EliminarProductoCarrito.as_view()),
    path('order/consultarcarrito/cliente', ConsultarCarritoCliente.as_view()),
    path('order/carrito/cliente', ConsultarCarritoActualCliente.as_view()),
    path('order/carrito/cancelar/', CancelarCompra.as_view())
]
