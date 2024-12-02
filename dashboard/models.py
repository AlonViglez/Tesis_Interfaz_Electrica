from django.db import models
from login.models import Maestro, Usuario  # Asegúrate de que la aplicación login esté incluida en INSTALLED_APPS
from django.core.validators import RegexValidator

class AgendarFecha(models.Model):
    id_maestro = models.ForeignKey(Maestro, on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    clave_generada = models.CharField(max_length=100)
    limite_alumnos = models.IntegerField()
    clave_utilizada = models.IntegerField()
    fecha_solicitada = models.DateTimeField()
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
        return f'Agenda {self.id} - Maestro: {self.id_maestro.nombre} - Usuario: {self.id_alumno.nombre}'

#Almacenar datos extraídos del arduino
class DatosAlumno(models.Model):
    voltaje = models.FloatField()
    temperatura = models.FloatField()
    fecha = models.DateTimeField()
    id_alumno = models.CharField(max_length=9, validators=[RegexValidator(r'^\d{1,10}$')])

    def __str__(self):
        return str(self.id_alumno)

#Modelo para boton
class BotonEstado(models.Model):
    estado = models.BooleanField(default=False)  # False: Desactivado, True: Activado

class SensorData(models.Model):
    d1 = models.FloatField()
    d2 = models.FloatField()
    d3 = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"D1: {self.d1}, D2: {self.d2}, D3: {self.d3}, Timestamp: {self.timestamp}"