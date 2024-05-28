from django import forms
from . models import AgendarFecha #lo tomo de models y el nombre de la tabla
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class Maestrocitar(forms.ModelForm):
     class Meta:
        model = AgendarFecha
        fields = ['limite_alumnos', 'grado', 'grupo', 'fecha_solicitada', 'clave_generada', 'id_maestro', 'id_alumno']
        widgets = {
            'fecha_solicitada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    