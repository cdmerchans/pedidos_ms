from django.shortcuts import render
from .models import Person, Order, Inventario, DetallesOrder, EstadoOrder
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.views.generic.edit import CreateView, DeleteView, UpdateView , FormView , View
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse

from .serializers import PersonSerializer, InventarioSerializer, DetallesOrderSerializer, OrderSerializer, EstadoSerializer

# Create your views here.
@method_decorator(csrf_exempt, name='post')
class AgregarProductoCarrito (APIView):
    def post(self, request, *args, **kwargs):
        idproducto = request.data['id_inventario']
        order_old_test= Order.objects.all()
        id_new=0
        initial_estado = EstadoOrder('1')
        try:
            cliente_in_db = Person.objects.get(id_person = int(request.data['id_person']))
        except Person.DoesNotExist:
            return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)

        try:
            producto_in_db = Inventario.objects.get(id_inventario = idproducto)
        except Inventario.DoesNotExist:
            return Response({"message": "Producto no existe"},status=status.HTTP_404_NOT_FOUND)

        id_person_open = Person(int(request.data['id_person']))
        open_order = Order.objects.filter(id_person = id_person_open) & Order.objects.filter(estado_order = initial_estado)

        ids= 1
        id_lista=[]
        if open_order:
            for e in open_order:
                ids=e.id_order

            
        else: 
            if  order_old_test !=[]: 
                for venta in order_old_test:
                    id_lista.append(venta.id_order)
            if id_lista!=[]:
                ids = max(id_lista)
                order_old_end = Order.objects.get(id_order = ids)
                estado_old_end = order_old_end.estado_order.id_estado_order
                cliente_old_end = order_old_end.id_person.id_person
                id_person = int(request.data['id_person'])
                if estado_old_end == '2' or estado_old_end == '3' or estado_old_end == '4':
                    ids = ids +1
                elif estado_old_end == '1' and cliente_old_end == id_person:
                    ids = ids
                elif estado_old_end == '1' and cliente_old_end != id_person:
                    ids = ids +1

        initial_estado = EstadoOrder('1')
        id_person = Person(int(request.data['id_person']))
        order_in_db = Order(id_order = ids, id_person = id_person, precio_total = 0, address_order ='', estado_order = initial_estado)
        order_in_db.save()
        
        
        cantidad = request.data['cantidad']
        
        
        idproducto =Inventario(request.data['id_inventario'])
        actual_id_order = Order(ids)
        venta_old_test= DetallesOrder.objects.filter(id_order = actual_id_order) & DetallesOrder.objects.filter(id_inventario = idproducto)
        
        serializer = DetallesOrderSerializer(venta_old_test,many=True)
        precio = producto_in_db.precio_producto
        print(serializer.data)
        if serializer.data ==[]:            
            subtotal_new = cantidad * precio
            actual_id_order = Order(ids)
            producto_in_carrito = DetallesOrder(id_order = actual_id_order, id_inventario = idproducto, cantidad = cantidad, valor_total = subtotal_new)
            producto_in_carrito.save()
        else:
            for e in venta_old_test:
                cantidad_old = e.cantidad
                iddetalle=e.id_detalles_order
            pedido_actualizar= DetallesOrder.objects.get(id_detalles_order = iddetalle)
            cantidad = cantidad_old + cantidad
            subtotal_new = cantidad * precio
            actual_id_order = Order(ids)
            pedido_actualizar.cantidad = cantidad
            pedido_actualizar.valor_total = subtotal_new
            pedido_actualizar.save()
        
        return Response({"message": "Producto agregado"}, status=status.HTTP_201_CREATED)

class ConsultarCarrito(APIView):
    def get(self, request, *args, **kwargs):
        order_old_test= Order.objects.all()
        order_old_test_va=list(order_old_test.values())

        serializer = OrderSerializer(order_old_test,many=True)
        json = JSONRenderer().render(serializer.data)

        return JsonResponse(order_old_test_va, safe=False)


class ConsultarCarritoCliente(APIView):
    def get(self, request, *args, **kwargs):
        id_person = Person(int(request.data['id_person']))
        try:
            cliente_in_db = Person.objects.get(id_person = int(request.data['id_person']))
        except Person.DoesNotExist:
            return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)
        order_old_test= Order.objects.all().filter(id_person = id_person)
        prueba_order = order_old_test.values()
        prueba_order1 = list(prueba_order)

        serializer = OrderSerializer(order_old_test,many=True)

        if prueba_order1 ==[]:
            json = {"message": "El cliente no ha realizado pedidos"}
        else:
            json = prueba_order1

        return JsonResponse(json, safe=False)


class ConsultarCarritoActualCliente(APIView):
    def get(self, request, *args, **kwargs):
        id_person = Person(int(request.data['id_person']))
        try:
            cliente_in_db = Person.objects.get(id_person = int(request.data['id_person']))
        except Person.DoesNotExist:
            return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            order_in_db = Order.objects.get(id_order = request.data['id_order'])
        except Order.DoesNotExist:
            return Response({"message": "La orden no existe"}, status=status.HTTP_404_NOT_FOUND)

        actual_id_order = request.data['id_order']
        order_old_test= Order.objects.filter(id_order = actual_id_order) & Order.objects.filter(id_person = id_person)
        order_old_test_va=list(order_old_test.values())
        serializer = OrderSerializer(order_old_test,many=True)

        if order_old_test_va ==[]:
            json = {"message": "El cliente no ha realizado este pedido"}
        else:
            json = order_old_test_va
        

        return JsonResponse(json, safe=False)


@method_decorator(csrf_exempt, name='delete')
class EliminarProductoCarrito(APIView):
    def delete(self, request, *args, **kwargs):
        idproducto = request.data['id_inventario']

        idproducto =Inventario(request.data['id_inventario'])
        actual_id_order = Order(request.data['id_order'])
        venta_old_test= DetallesOrder.objects.filter(id_order = actual_id_order) & DetallesOrder.objects.filter(id_inventario = idproducto)
        print(venta_old_test)
        for e in venta_old_test:
            print(e.id_inventario.id_inventario)
            print(e.id_detalles_order)
        venta_old_test.delete()

        return Response({"message": "Producto eliminado"})

class ComprarVenta(APIView):
    def put(self, request, *args, **kwargs):
        id_order_f = int(request.data['id_order'])
        venta_old_test= Order.objects.get(id_order = id_order_f)
        suma = 0
        ordenes_old_test= DetallesOrder.objects.filter(id_order = id_order_f)
        for e in ordenes_old_test:
            suma = e.valor_total + suma
        venta_old_test.estado_order = EstadoOrder('2')
        venta_old_test.precio_total = suma
        venta_old_test.save()
        

        return Response({"message": "Compra realizada"}, status=status.HTTP_201_CREATED)

class CancelarCompra(APIView):
    def put(self, request, *args, **kwargs):
        id_order_f = int(request.data['id_order'])
        venta_old_test= Order.objects.get(id_order = id_order_f)
        suma = 0
        ordenes_old_test= DetallesOrder.objects.filter(id_order = id_order_f)
        for e in ordenes_old_test:
            suma = e.valor_total + suma
        venta_old_test.estado_order = EstadoOrder('4')
        venta_old_test.precio_total = suma
        venta_old_test.save()
        

        return Response({"message": "Compra cancelada"}, status=status.HTTP_200_OK)

            
