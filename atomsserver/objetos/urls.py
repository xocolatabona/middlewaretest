from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_object, name='add'),
    path('monitoreo/', views.monitoreo, name='monitoreo'),
    path('monitoreo/corregir/<int:idTrans>', views.corregirTransaccion, name="corregir"),
    path('buscarTalla/', views.buscarTalla, name="buscartalla"),
]