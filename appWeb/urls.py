from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required #Para autenticacion
from login import views as login_views
from dashboard import views as dashboard_views
#from login import views as registrar_views
#from login import views as autenticacion_views
#from login import views as logueado_views
#from login import views as registrar_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.home, name='home'),
    path('registrar/', login_views.registrar, name='registrar'),
    path('registrarMaestro/', login_views.registrarMaestro, name='registrarMaestro'),
    #path('registrarAlumno/', login_views.registrar, name='registrarAlumno'),
    path('autenticacion/', login_views.autenticacion, name='autenticacion'),
    path('logout/', login_views.logout_view, name='logout'),
    path('logueado/', login_views.logueado, name='logueado'),
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),  
    path('dashboardpulso/', dashboard_views.grafpulso, name='grafpulso'),
    path('dashboardlineal/', dashboard_views.graflineal, name='graflineal'),
    path('dashboardbarra/', dashboard_views.grafbarra, name='grafbarra'),
    path('dashboardmedidores/', dashboard_views.grafmedidores, name='grafmedidores'),
    path('dashboardagendar/', dashboard_views.grafagendar, name='grafagendar'),
    path('dashboardM/', dashboard_views.dashboardM, name='dashboardM'),  
    path('dashboardpulsoM/', dashboard_views.grafpulsoM, name='grafpulsoM'),
    path('dashboardlinealM/', dashboard_views.graflinealM, name='graflinealM'),
    path('dashboardbarraM/', dashboard_views.grafbarraM, name='grafbarraM'),
    path('dashboardmedidoresM/', dashboard_views.grafmedidoresM, name='grafmedidoresM'),
    path('solicitudes/', dashboard_views.solicitudes, name='solicitudes'),
    path('agendar_fecha_view/', dashboard_views.agendar_fecha_view, name='agendar_fecha_view'),
    path('chart-data/', dashboard_views.chart_data, name='chart-data'),
    path('connect-arduino/', dashboard_views.connect_arduino, name='connect_arduino'),
]



