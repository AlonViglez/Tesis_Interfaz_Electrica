from django.shortcuts import render,redirect
from login.models import Usuario,Maestro
from django.http import HttpResponse


#Checar si esta logueado sino mandarlo al home
def check_logueado(request, template_name):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
        return render(request, template_name,{'usuario': usuario})
    else:
        return redirect('home')
#seccion del alumno
def dashboard(request):
    return check_logueado(request, 'dashboard.html')

def grafpulso(request):
    return check_logueado(request, 'grafica_de_pulso.html')

def graflineal(request):
    return check_logueado(request, 'grafica_lineal.html')

def grafbarra(request):
    return check_logueado(request, 'grafbarra.html')

def grafmedidores(request):
    return check_logueado(request, 'grafmedidores.html')

def grafagendar(request):
    return check_logueado(request, 'agendar.html')

def dashboardM(request):
    return check_logueado(request, 'dashboardM.html')

def grafpulsoM(request):
    return check_logueado(request, 'grafica_de_pulsoM.html')

def graflinealM(request):
    return check_logueado(request, 'grafica_linealM.html')

def grafbarraM(request):
    return check_logueado(request, 'grafbarraM.html')

def grafmedidoresM(request):
    return check_logueado(request, 'grafmedidoresM.html')

def solicitudes(request):
    return check_logueado(request, 'solicitudes.html')

def chart(request):
    return check_logueado(request, 'simplechart.py')