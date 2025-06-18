from django.db import models
from django.db.models import  IntegerField

from AppsFincaBarillas.Operaciones.ventas.models import Venta
from AppsFincaBarillas.Catalogos.producto.models import producto

class DetalleVenta(models.Model):
    Id_DetalleVenta = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE, verbose_name="Producto")
    descripcion = models.CharField(max_length=100)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_producto = models.SmallIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.descripcion
    


def detalleVenta():
    return None