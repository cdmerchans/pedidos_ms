from django.db import models

# Create your models here.

class EstadoOrder(models.Model):
    id_estado_order = models.CharField(max_length=30, primary_key=True)
    descripcion_estado = models.CharField(max_length=150)

class Order(models.Model):
    id_order = models.BigAutoField(primary_key=True)
    id_person = models.BigIntegerField()
    precio_total = models.IntegerField()
    address_order = models.CharField(max_length=150)
    estado_order = models.ForeignKey(EstadoOrder, on_delete=models.CASCADE)

class DetallesOrder(models.Model):
    id_detalles_order = models.BigAutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_producto = models.BigIntegerField()
    cantidad = models.IntegerField()
    valor_total = models.IntegerField()



