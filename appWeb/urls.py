from django.contrib import admin
from django.urls import path, include
from login import views as login_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.home, name='home'),
    path('registrar/', login_views.registrar, name='registrar'), 
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
    path('solicitudes/', dashboard_views.solicitudes, name='solicitudes')
]



