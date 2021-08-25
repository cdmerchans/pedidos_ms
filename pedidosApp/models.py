from django.db import models

# Create your models here.

class Person(models.Model):
    id_person = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    super_user = models.BooleanField()
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()

class EstadoOrder(models.Model):
    id_estado_order = models.CharField(max_length=30, primary_key=True)
    descripcion_estado = models.CharField(max_length=150)

class Order(models.Model):
    id_order = models.BigAutoField(primary_key=True)
    id_person = models.ForeignKey(Person, on_delete=models.CASCADE)
    precio_total = models.IntegerField()
    address_order = models.CharField(max_length=150)
    estado_order = models.ForeignKey(EstadoOrder, on_delete=models.CASCADE)

class Inventario(models.Model):
    id_inventario = models.CharField(max_length=30, primary_key=True)
    nombre_producto = models.CharField(max_length=30)
    precio_producto = models.IntegerField()
    descripcion_producto = models.CharField(max_length=150)
    cantidad_inventario = models.IntegerField()
    categoria = models.CharField(max_length=50)

class DetallesOrder(models.Model):
    id_detalles_order = models.BigAutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valor_total = models.IntegerField()



