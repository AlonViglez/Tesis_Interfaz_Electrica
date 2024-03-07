from django.contrib import admin
from django.urls import path
from . import views #ruta de los archivos llamadas


urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/', views.saludo, name='saludo'),#en vez de poner path podemos solo llamandola por el nombre name='' (ruta estatica)
    path('despedida/',views.despedida, name='despedida'),
    path('adulto/<int:edad>/',views.adulto, name='adulto') #recepionar un parametro

]
