from django import forms
from .models import FormularioInscripcionHUT

class InscripcionForm(forms.ModelForm):
    codigo_pais = forms.CharField(label='Cod. país', max_length=3,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60px;'}))
    codigo_area = forms.CharField(label='Cod. área', max_length=5,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}))
    numero_telefono = forms.CharField(label='Nro. teléfono', max_length=15,
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 120px;'}))

    class Meta:
        model = FormularioInscripcionHUT
        fields = "__all__"
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'estadoCivil': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            'pastor': forms.TextInput(attrs={'class': 'form-control'}),
            'congregacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre y Apellido',
            'telefono': 'Teléfono (Con código de país y área ej: 54 3544 123456 )',
            'pais': 'País',
            'provincia': 'Provincia',
            'pastor':'Pastor / ra',
            'estadoCivil':'Estado Civil',
            'congregacion': 'Congregación'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['telefono'] = '+xx xxxx xxxxxx'
