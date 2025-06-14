from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta
from AppsFincaBarillas.Catalogos.cliente.models import Cliente

class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente  # tu modelo cliente
        fields = ['codigo', 'nombres', 'apellidos']


class VentaSerializer(ModelSerializer):
    cliente = ClienteSerializer()

    class Meta:
        model = Venta
        fields = ['id_venta','cliente','numero_venta','metodo_pago', 'fecha_venta','monto_total']
        # fields = '__all__'