from django.shortcuts import render
from .models import Order, DetallesOrder, EstadoOrder
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
import requests
import json

from .serializers import DetallesOrderSerializer, OrderSerializer, EstadoSerializer

# Create your views here.
@method_decorator(csrf_exempt, name='post')
class AgregarProductoCarrito (APIView):
    def post(self, request, *args, **kwargs):
        idproducto = request.data['id_producto']
        order_old_test= Order.objects.all()
        id_new=0
        initial_estado = EstadoOrder('1')
        usuario= request.data['id']
        parameters_person = {'id': usuario}
        urlperson = 'https://proyecto-autenticacion.herokuapp.com/buscar/'+ str(usuario)
        url_producto = 'https://proyecto-inventario-1.herokuapp.com/buscar/' + str(idproducto)
        parameters_producto = {'id_producto': idproducto}
        try:
            cliente_in= requests.get(urlperson)
            if cliente_in.status_code == 404:
                return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)
            results_cliente = json.loads(cliente_in.text)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
            

        try:
            page= requests.get(url_producto)
            if page.status_code == 404:
                return Response({"message": "Producto no existe"},status=status.HTTP_404_NOT_FOUND)
            print (page)
            results_producto = json.loads(page.text)
            print(type(results_producto))
            
            print(results_producto)
            #print(results_producto[0]['precio'])
            

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
            #return Response({"message": "Producto no existe"},status=status.HTTP_404_NOT_FOUND)
        cantidad_pedida = request.data['cantidad']
        precio = results_producto[0]['precio']
        nombre_producto = results_producto[0]['nombre']
        cantidad_db =results_producto[0]['cantidad']
        parameters1 = {  'id_producto': idproducto,
                        'cantidad': -cantidad_pedida
                    }
        print (parameters1)
        try:
            page= requests.put('https://proyecto-inventario-1.herokuapp.com/cantidad/', data=parameters1)
            if page.status_code == 406:
                    return Response({"message": "No hay suficientes productos en Stock"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif page.status_code == 404:
                return Response({"message": "El producto no existe"},status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        print (page)
        results = json.loads(page.text)
        print(results)
        id_person_open = request.data['id']
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
                cliente_old_end = order_old_end.id_person
                id_person = request.data['id']
                if estado_old_end == '2' or estado_old_end == '3' or estado_old_end == '4':
                    ids = ids +1
                elif estado_old_end == '1' and cliente_old_end == id_person:
                    ids = ids
                elif estado_old_end == '1' and cliente_old_end != id_person:
                    ids = ids +1

        initial_estado = EstadoOrder('1')
        id_person = request.data['id']
        order_in_db = Order(id_order = ids, id_person = id_person, precio_total = 0, address_order ='', estado_order = initial_estado)
        order_in_db.save()
        
        
        
        
        
        idproducto =request.data['id_producto']
        actual_id_order = Order(ids)
        venta_old_test= DetallesOrder.objects.filter(id_order = actual_id_order) & DetallesOrder.objects.filter(id_producto = idproducto)
        
        serializer = DetallesOrderSerializer(venta_old_test,many=True)
        print(serializer.data)
        if serializer.data ==[]:            
            subtotal_new = cantidad_pedida * precio
            actual_id_order = Order(ids)
            producto_in_carrito = DetallesOrder(id_order = actual_id_order, id_producto = idproducto, cantidad = cantidad_pedida, valor_total = subtotal_new)
            producto_in_carrito.save()
        else:
            for e in venta_old_test:
                cantidad_old = e.cantidad
                iddetalle=e.id_detalles_order
            pedido_actualizar= DetallesOrder.objects.get(id_detalles_order = iddetalle)
            cantidad1 = cantidad_old + cantidad_pedida
            subtotal_new = cantidad1 * precio
            actual_id_order = Order(ids)
            pedido_actualizar.cantidad = cantidad1
            pedido_actualizar.valor_total = subtotal_new
            pedido_actualizar.save()


        
        
        return Response({"message": "Producto agregado", "order": ids}, status=status.HTTP_201_CREATED)

class ConsultarCarrito(APIView):
    def get(self, request, *args, **kwargs):
        order_old_test= Order.objects.all()
        order_old_test_va=list(order_old_test.values())

        serializer = OrderSerializer(order_old_test,many=True)
        json2 = JSONRenderer().render(serializer.data)

        return JsonResponse(order_old_test_va, safe=False)

import json
class ConsultarCarritoCliente(APIView):
    def get(self, request, *args, **kwargs):
        id_person = request.query_params.get('id', None)
        #id_person = int(request.data['id'])
        parameters_person = {'id': id_person}
        urlperson = 'https://proyecto-autenticacion.herokuapp.com/buscar/'+ str(id_person)
        try:
            cliente_in= requests.get(urlperson)
            if cliente_in.status_code == 404:
                return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)
            results_cliente = json.loads(cliente_in.text)
        except requests.exceptions.HTTPError as err:
            #raise SystemExit(err)
            return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)



        order_old_test= Order.objects.all().filter(id_person = id_person)
        prueba_order = order_old_test.values()
        prueba_order1 = list(prueba_order)

        serializer = OrderSerializer(order_old_test,many=True)

        if prueba_order1 ==[]:
            json3 = {"message": "El cliente no ha realizado pedidos"}
        else:
            json3 = prueba_order1

        return JsonResponse(json3, safe=False)


class ConsultarCarritoActualCliente(APIView):
    def get(self, request, *args, **kwargs):
        print(request.data)
        id_person = request.query_params.get('id', None)
        #id_person = int(request.data['id'])
        parameters_person = {'username': id_person}
        urlperson = 'https://proyecto-autenticacion.herokuapp.com/buscar/'+ str(id_person)
        try:
            cliente_in= requests.get(urlperson)
            if cliente_in.status_code == 404:
                return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)
            results_cliente = json.loads(cliente_in.text)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
        try:
            id_order = request.query_params.get('id_order', None)
            order_in_db = Order.objects.get(id_order = id_order)
        except Order.DoesNotExist:
            return Response({"message": "La orden no existe"}, status=status.HTTP_404_NOT_FOUND)

        actual_id_order = Order(request.query_params.get('id_order', None))
        #actual_id_order = request.data['id_order']
        order_old_test= DetallesOrder.objects.filter(id_order = actual_id_order)
        order_old_test_va=list(order_old_test.values())
        serializer = OrderSerializer(order_old_test,many=True)

        if order_old_test_va ==[]:
            json4 = {"message": "El cliente no ha realizado este pedido"}
        else:
            json4 = order_old_test_va
        

        return JsonResponse(json4, safe=False)


@method_decorator(csrf_exempt, name='delete')
class EliminarProductoCarrito(APIView):
    def delete(self, request, *args, **kwargs):
        idproducto = request.query_params.get('id_producto', None)
        url_producto = 'https://proyecto-inventario-1.herokuapp.com/buscar/' + str(idproducto)
        parameters_producto = {'id_producto': idproducto}
        try:
            page= requests.get(url_producto)
            if page.status_code == 404:
                return Response({"message": "Producto no existe"},status=status.HTTP_404_NOT_FOUND)
            print (page)
            results_producto = json.loads(page.text)
            print(type(results_producto))
            print(results_producto)

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        precio = results_producto[0]['precio']
        nombre_producto = results_producto[0]['nombre']
        cantidad_db =results_producto[0]['cantidad']
        #idproducto = request.data['id_producto']
        
        #actual_id_order = Order(request.data['id_order'])
        actual_id_order = Order(request.query_params.get('id_order', None))
        venta_old_test= DetallesOrder.objects.filter(id_order = actual_id_order) & DetallesOrder.objects.filter(id_producto = idproducto)
        print(venta_old_test)
        for e in venta_old_test:
            print(e.id_producto)
            print(e.id_detalles_order)
            cantidad_pedida = e.cantidad
        venta_old_test.delete()

        parameters1 = {  'id_producto': idproducto,
                        'cantidad': cantidad_pedida
                    }
        print (parameters1)
        try:
            page= requests.put('https://proyecto-inventario-1.herokuapp.com/cantidad/', data=parameters1)
            if page.status_code == 406:
                    return Response({"message": "No hay suficientes productos en Stock"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            elif page.status_code == 404:
                return Response({"message": "El producto no existe"},status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        return Response({"message": "Producto eliminado"})

class ComprarVenta(APIView):
    def put(self, request, *args, **kwargs):
        id_order_f = request.data['id_order']
        venta_old_test= Order.objects.get(id_order = id_order_f)
        id_person = venta_old_test.id_person
        print(id_person)
        suma = 0
        ordenes_old_test= DetallesOrder.objects.filter(id_order = id_order_f)
        address = request.data['address_order']
        for e in ordenes_old_test:
            suma = e.valor_total + suma
        if address == "":
            urlperson = 'https://proyecto-autenticacion.herokuapp.com/buscar/'+ str(id_person)
            try:
                cliente_in= requests.get(urlperson)
                if cliente_in.status_code == 404:
                    return Response({"message": "Cliente no existe"}, status=status.HTTP_404_NOT_FOUND)
                results_cliente = json.loads(cliente_in.text)
                print(cliente_in)
                results_cliente = json.loads(cliente_in.text)
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            address =results_cliente[0]['address']        
        
        venta_old_test.estado_order = EstadoOrder('2')
        venta_old_test.precio_total = suma
        venta_old_test.address_order =address
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
            id_producto = e.id_producto
            cantidad_pedida = e.cantidad
            parameters1 = {  'id_producto': id_producto,
                            'cantidad': cantidad_pedida
                        }
            print (parameters1)
            try:
                page= requests.put('https://proyecto-inventario-1.herokuapp.com/cantidad/', data=parameters1)
                if page.status_code == 406:
                        return Response({"message": "No hay suficientes productos en Stock"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                elif page.status_code == 404:
                    return Response({"message": "El producto no existe"},status=status.HTTP_404_NOT_FOUND)
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

        venta_old_test.estado_order = EstadoOrder('4')
        venta_old_test.precio_total = suma
        venta_old_test.save()
        

        return Response({"message": "Compra cancelada"}, status=status.HTTP_200_OK)

            
