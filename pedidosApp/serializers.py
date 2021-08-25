from rest_framework import serializers
from .models import Person, Order, Inventario, DetallesOrder, EstadoOrder

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id_person', 'username', 'password', 'super_user','address','email','phone']


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoOrder
        fields = ['id_estado_order', 'descripcion_estado']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id_order', 'id_person_id', 'precio_total', 'address_order','estado_order']


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ['id_inventario', 'nombre_producto', 'precio_producto', 'descripcion_producto','cantidad_inventario','categoria']


class DetallesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesOrder
        fields = ['id_detalles_order', 'id_order', 'id_inventario', 'cantidad','valor_total']
