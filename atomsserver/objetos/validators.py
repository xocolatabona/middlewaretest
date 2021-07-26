from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
import json

def validate_tags(tag_string):
    tag_list = tag_string.rsplit(',')
    if len(tag_list) > 25:
        raise ValidationError(
            _("El objeto no puede tener más de 25 etiquetas"),
        )

def validate_tallas(talla_string):
    talla_list = talla_string.rsplit(',')
    regex = '^\-?\d+$' #regex para validar que la talla es un número entero
    for t in talla_list:
        if re.search(regex, t) == None:
            raise ValidationError(
                _("La lista contiene una talla inválida"),
            )

def validate_costo(costo):
    if not costo > 0:
        raise ValidationError(
            _("El costo no puede ser igual o menor a 0"),
        )

def validate_base64(base64_string):
    base64_list = json.loads(base64_string)
    regex = '^(?:[A-Za-z\d+/]{4})*(?:[A-Za-z\d+/]{3}=|[A-Za-z\d+/]{2}==)?$'
    for b in base64_list:
        if re.search(regex, b) == None:
            raise ValidationError(
                _("La imagen no está correctamente codificada en base64"),
            )