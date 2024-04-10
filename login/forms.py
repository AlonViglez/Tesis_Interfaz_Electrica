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
            'materia',
            'numero_cuenta',
        ]
        #Mensajes de error
        error_messages = {
            'email': {
                'unique': 'Este correo electrónico ya está registrado.',
            },
            'numero_cuenta': {
                'unique': 'Este número de cuenta ya está registrado.',
            },
        }
        
    #VALIDACIONES
    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError(self.fields['email'].error_messages['unique'], code='unique')
        return email
    
    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data['numero_cuenta']
        if Usuario.objects.filter(numero_cuenta=numero_cuenta).exists():
            raise ValidationError(self.fields['numero_cuenta'].error_messages['unique'], code='unique')
        return numero_cuenta
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reppassword = cleaned_data.get('reppassword')
        if password and reppassword and password != reppassword:
            raise ValidationError('Las contraseñas no coinciden')

        email = cleaned_data.get('email')
        numero_cuenta = cleaned_data.get('numero_cuenta')
        if Usuario.objects.filter(email=email).exists() or Usuario.objects.filter(numero_cuenta=numero_cuenta).exists():
            raise ValidationError('Este correo electrónico o número de cuenta ya están registrados')

        return cleaned_data
    
    #FUNCION PARA GUARDAR SATISFACTORIAMENTE
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
            'especialidad',
            'numero_cuenta',
        ]
        #Mensajes de error
        error_messages = {
            'email': {
                'unique': 'Este correo electrónico ya está registrado.',
            },
            'numero_cuenta': {
                'unique': 'Este número de cuenta ya está registrado.',
            },
        }
        
    #VALIDACIONES
    def clean_email(self):
        email = self.cleaned_data['email']
        if Maestro.objects.filter(email=email).exists():
            raise ValidationError(self.fields['email'].error_messages['unique'], code='unique')
        return email
    
    def clean_numero_cuenta(self):
        numero_cuenta = self.cleaned_data['numero_cuenta']
        if Maestro.objects.filter(numero_cuenta=numero_cuenta).exists():
            raise ValidationError(self.fields['numero_cuenta'].error_messages['unique'], code='unique')
        return numero_cuenta
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reppassword = cleaned_data.get('reppassword')
        if password and reppassword and password != reppassword:
            raise ValidationError('Las contraseñas no coinciden')

        email = cleaned_data.get('email')
        numero_cuenta = cleaned_data.get('numero_cuenta')
        if Maestro.objects.filter(email=email).exists() or Usuario.objects.filter(numero_cuenta=numero_cuenta).exists():
            raise ValidationError('Este correo electrónico o número de cuenta ya están registrados')

        return cleaned_data
    
    #FUNCION PARA GUARDAR SATISFACTORIAMENTE
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance