from django.shortcuts import render
#from django.contrib.auth.forms import UserCreationForm #Clase para autenticacion y formulario
#from django.contrib.auth.models import User #Clase para registrar usuarios
from django.http import HttpResponse
from . forms import UsuarioForm, MaestroForm #Uso de mi formulario
from django.contrib.auth.hashers import make_password #Hashear
from django.shortcuts import render, redirect #Redireccionar
from .models import Usuario, Maestro #Uso del modelo de la tabla
from django.contrib.auth.hashers import check_password #Para contraseña hasheada loguearse
from django.contrib import messages #Mostrar mensajes en html
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your tests here.
def home(request):  
    if 'usuario_id' in request.session: #Funcion para home redireccionamiento
        return redirect('logueado')
    else:
        return render(request, 'home.html')
'''
def registrar(request):   #Funcion para registrar usuario redireccionamiento
    if request.method == 'GET':
        return render(request, 'registrar.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password'] == request.POST['reppassword']:
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
            '''
#Registro alumno
def registrar(request): 
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data['password'])  # Hashear la contraseña algoritmo PBKDF2 (Password-Based Key Derivation Function 2) apuntado al diccionario de datos cleaned_data
            usuario.save()
            #Guardar datos y redirigir a la pagina logueada
            #return render(request, 'logueado.html', {'usuario': usuario})
            return redirect("logueado")
    else:
        form = UsuarioForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

#Autenticacion alumno
def autenticacion(request):
    # Obtener datos del formulario
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id
                return render(request, 'logueado.html', {'usuario': usuario})  # Pasar el usuario como contexto
            else:
                print("Contraseña incorrecta.")
                # Devolver el formulario con los datos del usuario
                return render(request, 'home.html', {'email': email, 'error_message': 'Contraseña incorrecta'})
        except Usuario.DoesNotExist:
            print("Usuario no encontrado.")
            # Devolver el formulario con los datos del usuario
            return render(request, 'home.html', {'email': email, 'error_message': 'Usuario no encontrado'})
    else:
        # Si no es una solicitud POST, simplemente devolver el formulario
        return redirect("home")

#Autenticacion maestro
def autenticacionMaestro(request):
    # Obtener datos del formulario
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Maestro.objects.get(email=email)
            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id
                return render(request, 'logueado.html', {'usuario': usuario})  # Pasar el usuario como contexto
            else:
                print("Contraseña incorrecta.")
                # Devolver el formulario con los datos del usuario
                return render(request, 'home.html', {'email': email, 'error_message': 'Contraseña incorrecta'})
        except Maestro.DoesNotExist:
            print("Usuario no encontrado.")
            # Devolver el formulario con los datos del usuario
            return render(request, 'home.html', {'email': email, 'error_message': 'Usuario no encontrado'})
    else:
        # Si no es una solicitud POST, simplemente devolver el formulario
        return redirect("home")
    
def logueado(request):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return render(request, 'logueado.html', {'usuario': usuario})
        except Usuario.DoesNotExist:
            # El usuario no existe en la base de datos, eliminar la sesión y redirigir al home
            del request.session['usuario_id']
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')


