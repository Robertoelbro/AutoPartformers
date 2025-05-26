from django.db import models

# Create your models here.
class Producto(models.Model):
    codprod = models.CharField(max_length = 10)
    nomprod = models.CharField(max_length = 100)
    precio = models.IntegerField(null = False)
    descripcion = models.TextField(max_length = 500)
    publicado = models.BooleanField(default = False)
    categoria = models.TextField(max_length = 200, default = 'Sin Categoría')

    def __str__(self):
        return self.nomprod
    def __unicode__(self):
        return self.nomprod