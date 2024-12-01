from django.db import models
from django.core.validators import RegexValidator
#Si se agrega una nueva tabla ejecutar en orden los comandos:
#Makemigrations
#Migrate

#Datos para el alumno
class Usuario(models.Model):
    #Campos de texto
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    #Campos numéricos
    numero_cuenta = models.CharField(max_length=9, validators=[RegexValidator(r'^\d{1,10}$')])
    #Campos contraseñas
    password = models.CharField(max_length=50)
    # Campos de grado y grupo
    grado_choices = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
    ]
    grupo_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    grado = models.CharField(max_length=1, choices=grado_choices,default='1')
    grupo = models.CharField(max_length=1, choices=grupo_choices,default='A')

    def __str__(self):
        return str(self.numero_cuenta)

#Datos para el maestro
class Maestro(models.Model):
    # Campos de texto
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    materia = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.email)