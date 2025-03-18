from django.db import models
from django.contrib.auth.models import AbstractUser

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
    image = models.ImageField(upload_to='productos/img/', verbose_name='Imagen', validators=[validar_extencion])
    
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

class Rol(models.Model):
    code = models.CharField(max_length=255, blank=True, verbose_name='Codigo')
    name = models.CharField(max_length=255, verbose_name='Nombre')

class User(AbstractUser):
    role = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='Roles')
    username = models.CharField(max_length=255, unique=True, verbose_name='Nombre de Usuario')
    email = models.EmailField(verbose_name='Correo Electrónico', unique=True)
    first_name = models.CharField(max_length=255, verbose_name='Nombre')
    last_name = models.CharField(max_length=255, verbose_name='Apellido')
    date_of_birth = models.DateField(verbose_name='Fecha de Nacimiento')
    password1 = models.CharField(max_length=255, verbose_name='Contraseña')
    password2 = models.CharField(max_length=255, verbose_name='Confirmar Contraseña')
    phone_number = models.CharField(max_length=255, verbose_name='Número de Teléfono')
    address = models.CharField(max_length=255, verbose_name='Dirección')
    image = models.ImageField(upload_to='usuarios/img/', verbose_name='Imagen', blank=True, null=True, validators=[validar_extencion])
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_image = User.objects.get(pk=self.pk)
                if old_image.image != self.image:
                    old_image.image.delete(save=False)
            except Item.DoesNotExist:
                pass 
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.username