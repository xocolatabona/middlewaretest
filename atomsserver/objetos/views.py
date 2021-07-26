from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.core.exceptions import ValidationError
import json
from json.decoder import JSONDecodeError
from .models import Objeto, Transaccion
from .forms import ObjetoForm
from django.views.decorators.csrf import csrf_exempt
from .util import mergeSort, busquedaBinaria
from datetime import datetime, timedelta
import time

# Create your views here.
def index(request):
    return render(request, "objetos/docs.html")

@csrf_exempt
def add_object(request):
    if request.method == 'POST':
        try:
            obj_data = json.loads(request.body)
            nombre_producto = obj_data['nombre_producto']
            sku = obj_data['sku']
            imagenes = obj_data['imagenes']
            tags = obj_data['tags']
            costo = obj_data['costo']
            estatus = obj_data['estatus']
            tallas = obj_data['tallas']
            #la fecha de creación se guarda sola al crear el modelo
            fecha_actualizacion = datetime.now()
        except KeyError:
            return HttpResponse("Falta info", status=400)
        except JSONDecodeError:
            return HttpResponse("JSON mal formado", status=400)
        else:
            try:
                obj = Objeto.objects.get(sku=obj_data['sku'])
            except KeyError:
                #almacenar bad request y regresar un 404
                return HttpResponse("JSON sin SKU", status=400)
            except Objeto.DoesNotExist:
                try:
                    obj = Objeto(nombre_producto=nombre_producto, sku=sku, imagenes=json.dumps(imagenes), tags=tags, costo=costo,
                    estatus=estatus, tallas=tallas, fecha_actualizacion=fecha_actualizacion)
                    obj.full_clean()
                    obj.save()
                    t = Transaccion(json=json.dumps(obj_data), accion='add', status=201, errores='', descripcion='Se añadió el objeto')
                    t.save()
                    return HttpResponse(status=201)
                except ValidationError as e:
                    t = Transaccion(json=json.dumps(obj_data), accion='add', status=404, errores=json.dumps(e.message_dict), descripcion='Fallo al añadir el objeto')
                    t.save()
                    return HttpResponse(e.message_dict, status="404")
            else:
                try:
                    obj.nombre_producto = nombre_producto
                    obj.imagenes = json.dumps(imagenes)
                    obj.tags = tags
                    obj.costo = costo
                    obj.estatus = estatus
                    obj.tallas = tallas
                    obj.fecha_actualizacion = fecha_actualizacion
                    obj.full_clean()
                    obj.save()
                    t = Transaccion(json=json.dumps(obj_data), accion='update', status=201, errores='', descripcion='Se actualizó el objeto')
                    t.save()
                    return HttpResponse(status=201)
                except ValidationError as e:
                    t = Transaccion(json=json.dumps(obj_data), accion='update', status=404, errores=json.dumps(e.message_dict), descripcion='Error al actualizar el objeto')
                    t.save()
                    return HttpResponse(e.message_dict, status="404")
    else:
        return Http404()

def monitoreo(request):
    transacciones = Transaccion.objects.order_by('-fecha_transaccion')
    context = {"transacciones": transacciones}
    return render(request, "objetos/monitoreo.html", context)

def corregirTransaccion(request, idTrans):
    if request.method == 'POST':
        try:
            obj = Objeto.objects.get(sku=request.POST['sku'])
            form = ObjetoForm(request.POST, instance=obj)
        except Objeto.DoesNotExist:
            form = ObjetoForm(request.POST)

        if form.is_valid():
            clnd_data = form.cleaned_data
            obj = Objeto(nombre_producto=clnd_data['nombre_producto'], sku=clnd_data['sku'], imagenes=json.dumps(clnd_data['imagenes']), 
                    tags=clnd_data['tags'], costo=clnd_data['costo'], estatus=clnd_data['estatus'], tallas=clnd_data['tallas'], fecha_actualizacion=datetime.now())
            t = Transaccion.objects.get(pk=idTrans)
            t.corregida = True
            t.save()
            return redirect('monitoreo')
    else:
        t = Transaccion.objects.get(pk=idTrans)
        obj_data = json.loads(t.json)
        nombre_producto = obj_data['nombre_producto']
        sku = obj_data['sku']
        imagenes = obj_data['imagenes']
        tags = obj_data['tags']
        costo = obj_data['costo']
        estatus = obj_data['estatus']
        tallas = obj_data['tallas']
        fecha_actualizacion = datetime.now()
        try:
            obj = Objeto.objects.get(sku=obj_data['sku'])
            obj.nombre_producto = nombre_producto
            obj.imagenes = json.dumps(imagenes)
            obj.tags = tags
            obj.costo = costo
            obj.estatus = estatus
            obj.tallas = tallas
            obj.fecha_actualizacion = fecha_actualizacion
        except Objeto.DoesNotExist:
            obj = Objeto(nombre_producto=nombre_producto, sku=sku, imagenes=json.dumps(imagenes), tags=tags, costo=costo,
                    estatus=estatus, tallas=tallas, fecha_actualizacion=fecha_actualizacion)
        form = ObjetoForm(instance=obj)
        return render(request, 'objetos/corregir_transaccion.html', {'form': form, 'idTr': idTrans, 'errores': json.loads(t.errores)})

    return render(request, 'objetos/corregir_transaccion.html', {'form': form, 'idTr': idTrans})

@csrf_exempt
def buscarTalla(request):
    obj_data = json.loads(request.body)
    try:
        obj = Objeto.objects.get(sku=obj_data["sku"])
    except Objeto.DoesNotExist:
        return JsonResponse({"resultado": "No existe ningún objeto con ese SKU."}, safe=False)
    else:
        start_time = datetime.now().microsecond
        tallas_ord = mergeSort(obj.tallas.rsplit(","))
        obj.tallas = ','.join(map(str, tallas_ord))
        obj.save()
        try:
            busqueda = busquedaBinaria(tallas_ord, obj_data["talla"])
        except KeyError:
            return JsonResponse({"resultado": "No se ha proporcionado un parámetro talla válido"}, safe=False)
        tiempo = datetime.now().microsecond - start_time
        data = {'tallas_ordenadas': tallas_ord, 'resultado': busqueda, 'tiempo_busqueda': str(tiempo/1000) + " ms"}
        t = Transaccion(json=json.dumps(obj_data), accion='UD', status=201, errores='', descripcion='Se ordenó la lista de tallas')
        t.save()
        return JsonResponse(data, safe=False)
