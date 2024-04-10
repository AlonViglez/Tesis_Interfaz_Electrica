from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required #Para autenticacion
from login import views as login_views
#from login import views as registrar_views
#from login import views as autenticacion_views
#from login import views as logueado_views
#from login import views as registrar_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.home, name='home'),
    path('registrar/', login_views.registrar, name='registrar'),
    #path('registrarMaestro/', login_views.registrarMaestro, name='registrarMaestro'),
    #path('registrarAlumno/', login_views.registrar, name='registrarAlumno'),
    path('autenticacion/', login_views.autenticacion, name='autenticacion'),
    path('logout/', login_views.logout_view, name='logout'),
    path('logueado/', login_views.logueado, name='logueado'),
]
