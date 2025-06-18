from django.db import models
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto

class producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigoCultivo = models.CharField(max_length=6, unique=True)  # Código único del producto
    nombre = models.CharField(max_length=32)
    tipoProductoId = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    FechaSiembra = models.DateTimeField(auto_now_add=True)
    CantidadDisponible = models.IntegerField()  # Cantidad disponible del producto
    CantidadMinima = models.IntegerField()  # Cantidad mínima del producto
    precioVenta= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Precio de venta del producto
    estado = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.codigoCultivo}-{self.nombre}'

    class Meta:
        db_table = 'producto_producto'  # Asegúrate de que el nombre de la tabla es correcto

