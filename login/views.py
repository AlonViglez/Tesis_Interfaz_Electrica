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
            return redirect("home")
    else:
        form = UsuarioForm()
    return render(request, 'register.html', {'form': form})

#Registro maestro
def registrarMaestro(request): 
    if request.method == 'POST':
        form = MaestroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data['password'])  # Hashear la contraseña algoritmo PBKDF2 (Password-Based Key Derivation Function 2) apuntado al diccionario de datos cleaned_data
            usuario.save()
            #Guardar datos y redirigir a la pagina logueada
            #return render(request, 'logueado.html', {'usuario': usuario})
            return redirect("home")
    else:
        form = MaestroForm()
    return render(request, 'register_maestro.html', {'form': form})

#Autenticacion alumno
def autenticacion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.password):
                # Guardar el ID y el tipo en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['tipo_usuario'] = 'alumno'
                return redirect('logueado')
            else:
                print("Contraseña incorrecta.")
                return render(request, 'home.html', {
                    'email': email,
                    'error_message': 'Contraseña incorrecta'
                })
        except Usuario.DoesNotExist:
            print("Usuario no encontrado como alumno. Intentando como maestro.")
            return autenticacionMaestro(request)
    else:
        return redirect('home')
    
#Autenticacion maestro
def autenticacionMaestro(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Maestro.objects.get(email=email)
            if check_password(password, usuario.password):
                # Guardar el ID y el tipo en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['tipo_usuario'] = 'maestro'
                return redirect('logueado')
            else:
                print("Contraseña incorrecta.")
                return render(request, 'home.html', {
                    'email': email,
                    'error_message': 'Contraseña incorrecta'
                })
        except Maestro.DoesNotExist:
            print("Usuario no encontrado.")
            return render(request, 'home.html', {
                'email': email,
                'error_message': 'Usuario no encontrado'
            })
    else:
        return redirect('home')

#Logueo del alumno  
def logueado(request):
    if 'usuario_id' in request.session and 'tipo_usuario' in request.session:
        usuario_id = request.session['usuario_id']
        tipo_usuario = request.session['tipo_usuario']

        if tipo_usuario == 'maestro':
            try:
                usuario = Maestro.objects.get(id=usuario_id)
                return render(request, 'grafica_de_pulsoM.html', {'usuario': usuario})
            except Maestro.DoesNotExist:
                # Si el maestro no existe, eliminamos la sesión y redirigimos
                del request.session['usuario_id']
                del request.session['tipo_usuario']
                return redirect('home')

        elif tipo_usuario == 'alumno':
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                return render(request, 'grafica_de_pulso.html', {'usuario': usuario})
            except Usuario.DoesNotExist:
                # Si el alumno no existe, eliminamos la sesión y redirigimos
                del request.session['usuario_id']
                del request.session['tipo_usuario']
                return redirect('home')
    # Si no hay sesión, redirigir al home
    return redirect('home')

#Cerrar sesion
def logout_view(request):
    logout(request)
    return redirect('home')


