from django.db import models

class TipoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=6, unique=True)  # Código único del tipo de producto
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


# Create your models here.
