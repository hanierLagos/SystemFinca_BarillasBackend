from django.contrib import admin

from AppsFincaBarillas.Catalogos.producto.models import producto

@admin.register(producto)
class productoAdmin(admin.ModelAdmin):
    list_display = [
        'id_producto',
        'codigoCultivo',
        'nombre',
        'tipoProductoId',
        'FechaSiembra',
        'CantidadDisponible',  
        'CantidadMinima',      
        'estado'
    ]
    search_fields = ['codigoCultivo']
    list_filter = ['estado',]
# Register your models here.
