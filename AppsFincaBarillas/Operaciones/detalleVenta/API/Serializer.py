from rest_framework.serializers import ModelSerializer, ValidationError
from AppsFincaBarillas.Operaciones.detalleVenta.models import DetalleVenta
from AppsFincaBarillas.Catalogos.producto.models import producto

class DetalleVentaSerializer(ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['Id_DetalleVenta', 'venta', 'producto', 'descripcion', 'precio_producto', 'cantidad_producto', 'sub_total']
        read_only_fields = ['sub_total']
