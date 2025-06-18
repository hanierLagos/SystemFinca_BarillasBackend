from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta
from AppsFincaBarillas.Catalogos.cliente.models import Cliente
from rest_framework import serializers

class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente  # tu modelo cliente
        fields = ['codigo', 'nombres', 'apellidos']
 

class VentaSerializer(ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    class Meta:
        model = Venta
        fields = ['id_venta','cliente','numero_venta','metodo_pago', 'fecha_venta','monto_total', 'estado']
        # fields = '__all__'