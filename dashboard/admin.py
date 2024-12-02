from django.contrib import admin
from .models import AgendarFecha
from .models import DatosAlumno
from .models import BotonEstado
from .models import SensorData

admin.site.register(AgendarFecha)
admin.site.register(DatosAlumno)
admin.site.register(BotonEstado)
admin.site.register(SensorData)

