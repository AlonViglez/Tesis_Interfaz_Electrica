from django.contrib import admin
from django.urls import path, include
from login import views as login_views
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_views.home, name='home'),
    path('registrar/', login_views.registrar, name='registrar'),   
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),  
]



