from rest_framework import serializers
from .models import Order, DetallesOrder, EstadoOrder


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoOrder
        fields = ['id_estado_order', 'descripcion_estado']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id_order', 'id_person', 'precio_total', 'address_order','estado_order']


class DetallesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesOrder
        fields = ['id_detalles_order', 'id_order', 'id_producto', 'cantidad','valor_total']
