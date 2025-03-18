from django.db import models

def validar_extencion(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Por favor inserte un archivo png, jpg o jpeg para continuar')

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Añadido en')
    image = models.ImageField(upload_to='productos/img/', verbose_name='Imagen')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_item = Item.objects.get(pk=self.pk)
                if old_item.image != self.image:
                    old_item.image.delete(save=False)
            except Item.DoesNotExist:
                pass 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)