from django.db import models
from AppsFincaBarillas.Catalogos.cliente.models import Cliente

class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)  # es el numero de  `pedido` autogenerado
    codigo_pedido = models.CharField(max_length=6, unique=True)  # Código único del pedido
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    fecha_pedido = models.DateField()  # Almacena la fecha del pedido
    estado = models.CharField(max_length=32)

    def __int__(self):
        return int(self.id_pedido)  # Usar str() para evitar error de retorno no string


def pedidos():
    return None