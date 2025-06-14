from rest_framework import serializers
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ['id', 'codigo', 'description'] 