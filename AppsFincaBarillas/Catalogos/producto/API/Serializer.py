from rest_framework import serializers
from AppsFincaBarillas.Catalogos.producto.models import producto
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto

class ProductoSerializer(serializers.ModelSerializer):
    tipoProductoDescripcion = serializers.CharField(source='tipoProductoId.description', read_only=True)
    tipoProductoId = serializers.PrimaryKeyRelatedField(queryset=TipoProducto.objects.all(), write_only=True)

    class Meta:
        model = producto
        fields = [
            'id_producto',
            'codigoCultivo',
            'nombre',
            'tipoProductoId',
            'tipoProductoDescripcion',
            'FechaSiembra',
            'CantidadDisponible',
            'CantidadMinima',
            'estado'
        ]
