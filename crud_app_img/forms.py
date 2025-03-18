from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }