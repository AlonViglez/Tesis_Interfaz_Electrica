from django import forms
from . models import Usuario
from . models import Maestro
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    reppassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'email',
            'password',
            'numero_cuenta',
            'grado',
            'grupo',
        ]
        # Mensajes de error
        error_messages = {
            'email': {
                'unique': 'Este correo electrónico ya está registrado.',
            },
            'numero_cuenta': {
                'unique': 'Este número de cuenta ya está registrado.',
            },
        }

    # VALIDACIONES
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and (Usuario.objects.filter(email=email).exists() or Maestro.objects.filter(email=email).exists()):
            self.add_error('email', self.fields['email'].error_messages['unique'])
        return email

    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data.get('numero_cuenta')
        if numero_cuenta and Usuario.objects.filter(numero_cuenta=numero_cuenta).exists():
            self.add_error('numero_cuenta', self.fields['numero_cuenta'].error_messages['unique'])
        return numero_cuenta

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reppassword = cleaned_data.get('reppassword')
        if password and reppassword and password != reppassword:
            self.add_error('reppassword', 'Las contraseñas no coinciden')
        return cleaned_data

    # FUNCION PARA GUARDAR SATISFACTORIAMENTE
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance

class MaestroForm(forms.ModelForm):
    reppassword = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput())

    class Meta:
        model = Maestro
        fields = [
            'nombre',
            'email',
            'password',
            'materia',
        ]
        # Mensajes de error
        error_messages = {
            'email': {
                'unique': 'Este correo electrónico ya está registrado.',
            },
        }

    # VALIDACIONES
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and (Maestro.objects.filter(email=email).exists() or Usuario.objects.filter(email=email).exists()):
            self.add_error('email', self.fields['email'].error_messages['unique'])
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reppassword = cleaned_data.get('reppassword')
        if password and reppassword and password != reppassword:
            self.add_error('reppassword', 'Las contraseñas no coinciden')
        return cleaned_data

    # FUNCION PARA GUARDAR SATISFACTORIAMENTE
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance
