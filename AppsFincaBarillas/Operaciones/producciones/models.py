
from django.db import models
from AppsFincaBarillas.Catalogos.producto.models import producto

class Producciones(models.Model):
    Id_produccion = models.AutoField(primary_key=True)
    codigo_produccion = models.CharField(max_length=32, unique=True)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    calidad_cosecha = models.CharField(max_length=50)
    fecha_produccion = models.DateTimeField(auto_now_add=True)
    cantidad_producida = models.SmallIntegerField()
    lapso_produccion = models.DurationField()

    # Actualiza la cantidad disponible de los productos después de cada producción
    def save(self, *args, **kwargs):
        if self._state.adding:
            self.producto.CantidadDisponible += self.cantidad_producida
            self.producto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        
        return self.codigo_produccion


def producciones():
    return None