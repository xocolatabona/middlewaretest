from django.db import models
from .validators import *

# Create your models here.
class Objeto(models.Model):
    nombre_producto = models.CharField(max_length=300)
    sku = models.CharField(max_length=20, unique=True)
    imagenes = models.TextField(validators=[validate_base64], default='')
    tags = models.TextField(validators=[validate_tags])
    costo = models.FloatField(validators=[validate_costo])
    ACTIVE = 'active'
    ARCHIVED = 'archived'
    DRAFT = 'draft'
    ESTATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (ARCHIVED, 'Archived'),
        (DRAFT, 'Draft'),
    ]
    estatus = models.CharField(
        max_length=8,
        choices=ESTATUS_CHOICES,
    ) 
    tallas = models.TextField(validators=[validate_tallas])
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_actualizacion = models.DateTimeField()

class Transaccion(models.Model):
    fecha_transaccion = models.DateTimeField(auto_now=True)
    ADD = 'add'
    UPDATE = 'update'
    ACTION_CHOICES = [
        (ADD, 'Add'),
        (UPDATE, 'Update')
    ]
    accion = models.CharField(
        max_length=7,
        choices=ACTION_CHOICES,
        default=ADD,
    )
    json = models.TextField()
    status = models.IntegerField()
    errores = models.TextField()
    descripcion = models.TextField(default='')
    corregida = models.BooleanField(default=False)
