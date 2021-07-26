from django.forms import ModelForm
from .models import Objeto

class ObjetoForm(ModelForm):
    class Meta:
        model = Objeto
        fields = ['nombre_producto', 'sku', 'imagenes', 'tags', 'costo', 'estatus', 'tallas']