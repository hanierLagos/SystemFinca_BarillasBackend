from django.db import models
from AppsFincaBarillas.Catalogos.cliente.models import Cliente

class Pedidos(models.Model):
    id_pedido = models.IntegerField(primary_key=True)  # Generar el ID automáticamente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    fecha_pedido = models.DateField()  # Almacena la fecha del pedido
    estado = models.CharField(max_length=32)

    def __str__(self):
        return str(self.id_pedido)  # Usar str() para evitar error de retorno no string
