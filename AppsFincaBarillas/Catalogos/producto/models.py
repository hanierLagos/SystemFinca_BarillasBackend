from django.db import models

from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto


class producto(models.Model):
    id_producto=models.IntegerField(primary_key=True)
    codigoCultivo= models.CharField(max_length=6)
    nombre = models.CharField(max_length=32)
    tipoProductoId= models.ForeignKey(TipoProducto,on_delete=models.RESTRICT)
    FechaSiembra = models.DateTimeField(auto_now_add= True)
    estado = models.SmallIntegerField()


    def __str__(self):
        return self.codigoCultivo

# Create your models here.
