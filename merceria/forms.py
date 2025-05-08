from django import forms
from .models import Producto
from django.core.validators import MinValueValidator

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'precio': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Ej. 89.99'
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'precio': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'imagen': 'Imagen del Producto',
        }
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero")
        return round(precio, 2)