from django.db import models
from django.core.validators import RegexValidator

class Usuario(models.Model):
    #Campos de texto
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    materia = models.CharField(max_length=30)

    #Campos numéricos
    numero_cuenta = models.CharField(max_length=9, validators=[RegexValidator(r'^\d{1,10}$')])
    #Campos contraseñas
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.numero_cuenta)

