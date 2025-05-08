from django.db import models

# Create your models here.
class Producto(models.Model):
    class Categoria(models.TextChoices):
        TELAS = 'TELAS', 'Telas'
        MERCERIA = 'MERCERIA', 'Mercería'
        ACCESORIOS = 'ACCESORIOS', 'Accesorios'
        DECORACION = 'DECORACION', 'Decoracion'
        HOGAR = 'HOGAR', 'Hogar'

    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    imagen = models.ImageField(upload_to='images/',verbose_name="Imagen", null=True)
    precio = models.DecimalField(max_digits=10,verbose_name="Precio", decimal_places=2)
    descripcion = models.TextField(max_length=100, verbose_name="Descripcion")
    categoria = models.CharField(
        max_length=30,
        choices=Categoria.choices,
        verbose_name="Categoría"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en stock")  # Nuevo campo
    def esta_agotado(self):
        return self.stock == 0
    # Elimina el método __str__ duplicado y mejora el existente:
    def __str__(self):
        estado = "AGOTADO" if self.esta_agotado() else f"{self.stock} disponibles"
        return f"{self.nombre} - {self.categoria} ({estado})"

    def delete(self, using = None, keep_parents =False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
