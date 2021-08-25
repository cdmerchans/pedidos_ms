from django.contrib import admin
from .models import Person, Order, Inventario, DetallesOrder, EstadoOrder

# Register your models here.
admin.site.register(Person)
admin.site.register(Order)
admin.site.register(Inventario)
admin.site.register(DetallesOrder)
admin.site.register(EstadoOrder)
