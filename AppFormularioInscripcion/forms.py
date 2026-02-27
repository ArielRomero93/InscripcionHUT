
from django import forms
from django.contrib.auth.hashers import make_password
from .models import FormularioInscripcionHUT, FormularioDeDecision, Usuario, Voluntario
from django.core.exceptions import ValidationError
import re

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email','password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
            'role': forms.Select(choices=Usuario.ROLES),
        }

    def clean_password(self):
        # Asegúrate de hashear la contraseña antes de guardarla
        password = self.cleaned_data.get('password')
        return make_password(password)


class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(max_length=150, label='Usuario')
    email = forms.EmailField()

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Validar que la contraseña tenga al menos 12 caracteres
        if len(password1) < 12:
            raise ValidationError("La contraseña debe tener al menos 12 caracteres.")

        # Validar que la contraseña tenga al menos 2 letras mayúsculas
        if len(re.findall(r'[A-Z]', password1)) < 2:
            raise ValidationError("La contraseña debe tener al menos 2 letras mayúsculas.")

        # Validar que la contraseña tenga al menos 2 números
        if len(re.findall(r'\d', password1)) < 2:
            raise ValidationError("La contraseña debe tener al menos 2 números.")

        # Validar que la contraseña tenga al menos 2 caracteres especiales
        if len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password1)) < 2:
            raise ValidationError("La contraseña debe tener al menos 2 caracteres especiales.")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2











class InscripcionForm(forms.ModelForm):
    codigo_pais = forms.CharField(label='Cod. país (sin + y 9)', max_length=3,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60px;'}))
    codigo_area = forms.CharField(label='Cod. área (sin 0)', max_length=5,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}))
    numero_telefono = forms.CharField(label='Nro. teléfono', max_length=15,
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 120px;'}))

    class Meta:
        model = FormularioInscripcionHUT
        fields = "__all__"
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
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
            'nombre': 'Nombre',
            'apellido': 'Apellido',
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


class DecisionForm(forms.ModelForm):
    class Meta:
        model = FormularioDeDecision
        fields = "__all__"
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profesionOcupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'servicioElegido': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'E-mail',
            'profesionOcupacion': 'Profesion / Ocupacion',
            'servicioElegido': 'Oportunidades de Servicio',
            'telefono': 'Telefono'
        }


class VoluntarioForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        exclude = []
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'areas_interes': forms.CheckboxSelectMultiple(),
            'foto_rostro': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean_foto_rostro(self):
        foto = self.cleaned_data.get('foto_rostro')
        if foto:
            if foto.size > 3 * 1024 * 1024:  # 3MB máximo
                raise forms.ValidationError("La imagen no debe superar los 3MB.")
        return foto
