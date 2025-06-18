from django.db import models
from AppsFincaBarillas.Catalogos.cliente.models import Cliente  # Asegúrate de que Cliente esté bien importado

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)  # Numero autogenerado
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con la tabla Cliente
    numero_venta = models.CharField(max_length=10, unique=True)  # Número único de venta
    metodo_pago = models.CharField(max_length=50)  # Método de pago
    fecha_venta = models.DateTimeField()  # Fecha de la venta
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)  # Usar DecimalField para valores monetarios
    estado = models.BooleanField(default=True)  # Estado de la venta, por defecto True (activa)

    def __str__(self):
        return self.numero_venta  # Devolver el número de venta como representación en cadena de texto

