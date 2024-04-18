from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#seccion del alumno
def dashboard(request):  
    return render(request, 'dashboard.html')
def grafpulso(request):
    return render(request, 'grafica_de_pulso.html')
def graflineal(request):
    return render(request, 'grafica_lineal.html')
def grafbarra(request):
    return render(request, 'grafbarra.html')
def grafmedidores(request):
    return render(request, 'grafmedidores.html')
def grafagendar(request):
    return render(request, 'agendar.html')
def dashboardM(request): 
    return render(request, 'dashboardM.html')
def grafpulsoM(request):
    return render(request, 'grafica_de_pulsoM.html')
def graflinealM(request):
    return render(request, 'grafica_linealM.html')
def grafbarraM(request):
    return render(request, 'grafbarraM.html')
def grafmedidoresM(request):
    return render(request, 'grafmedidoresM.html')
def solicitudes(request):
    return render(request, 'solicitudes.html')