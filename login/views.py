from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm #Clase para autenticacion y formulario
from django.contrib.auth.models import User #Clase para registrar usuarios
from django.http import HttpResponse


# Create your tests here.
def home(request):   #Funcion para home redireccionamiento
    return render(request, 'home.html')

def registrar(request):   #Funcion para registrar usuario redireccionamiento
    if request.method == 'GET':
        return render(request, 'registrar.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
           try:
                # registro usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1']) #Crear objeto user
                user.save()
                return HttpResponse('Usuario creado correctamente')
           except:
               return render(request, 'registrar.html',{
                'form': UserCreationForm,
                "error": 'El usuario ya existe'
            })
        return render(request, 'registrar.html',{
                'form': UserCreationForm,
                "error": 'Contraseñas no coinciden'
            })
        
