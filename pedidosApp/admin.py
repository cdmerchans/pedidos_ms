from django.contrib import admin
from .models import Order, DetallesOrder, EstadoOrder

# Register your models here.
admin.site.register(Order)
admin.site.register(DetallesOrder)
admin.site.register(EstadoOrder)
