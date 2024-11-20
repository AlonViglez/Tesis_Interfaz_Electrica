from django.shortcuts import render,redirect
from login.models import Usuario,Maestro
from django.http import HttpResponse
from django.http import JsonResponse
import serial
import re
import random
import datetime
import time
from . forms import Maestrocitar
from .models import DatosAlumno  # Modelo de la tabla alumnos
#from . forms import registrarAgenda #Uso de mi formulario


#Checar si esta logueado el alumno sino mandarlo al home
def check_logueado(request, template_name, filtrar_datos=False):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
        # Guardar numero_cuenta en la sesión que se usará para identificar quien esta guardando los datos
        request.session['numero_cuenta'] = usuario.numero_cuenta
        # Filtrar DatosAlumno solo si filtrar_datos es True
        if filtrar_datos:
            datos = DatosAlumno.objects.filter(id_alumno=usuario.numero_cuenta) #Filtrar datos del alumno por su numero de cuenta
            return render(request, template_name, {'usuario': usuario, 'datos': datos}) #Enviar al html junto con ambos datos
        
        return render(request, template_name, {'usuario': usuario}) #Enviar al html solo los datos del usuario
    else:
        return redirect('home')
#Checar si esta logueado el maestro sino mandarlo al home
def check_logueado_Maestro(request, template_name):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Maestro.objects.get(id=usuario_id)
        return render(request, template_name,{'usuario': usuario})
    else:
        return redirect('home')
#Registro maestro
def agendar_fecha_view(request):
    if request.method == 'POST':
        form = Maestrocitar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboardM')  # Redirigir a una página de éxito
    else:
        form = Maestrocitar()
    return render(request, 'agendar_fecha.html', {'form': form})
#Seccion del alumno
def dashboard(request):
    return check_logueado(request, 'dashboard.html') #Enviar a la funcion para checar si esta logueado (se manda el request y el html)

def grafpulso(request):
    return check_logueado(request, 'grafica_de_pulso.html')

def graflineal(request):
    return check_logueado(request, 'grafica_lineal.html')

def grafbarra(request):
    return check_logueado(request, 'grafbarra.html')

def grafmedidores(request):
    return check_logueado(request, 'grafmedidores.html')

#Seccion Maestros
def grafagendar(request):
    return check_logueado(request, 'agendar.html')

def dashboardM(request):
    return check_logueado_Maestro(request, 'dashboardM.html')

def grafpulsoM(request):
    return check_logueado_Maestro(request, 'grafica_de_pulsoM.html')

def graflinealM(request):
    return check_logueado_Maestro(request, 'grafica_linealM.html')

def grafbarraM(request):
    return check_logueado_Maestro(request, 'grafbarraM.html')

def grafmedidoresM(request):
    return check_logueado_Maestro(request, 'grafmedidoresM.html')

def solicitudes(request):
    return check_logueado(request, 'solicitudes.html')

def historial_view(request):
    return check_logueado(request, 'historial_graficas.html', filtrar_datos=True)

def chart(request):
    return check_logueado(request, 'simplechart.py')
# Variables globales para el puerto serial
ser = None
serial_available = False

# Variables auxiliares
temp_values = {
    "D1": None,
    "D2": None,
    "D3": None
}
invalid_line_count = 0
MAX_INVALID_LINES = 5


def connect_serial():
    """Conecta al puerto serial."""
    global ser, serial_available
    try:
        if ser is None or not ser.isOpen():
            ser = serial.Serial('COM7', 9600, timeout=1)
            serial_available = True
            print("Puerto serial conectado correctamente.")
    except serial.SerialException as e:
        print(f"Error al conectar al puerto serial: {e}")
        ser = None
        serial_available = False


def disconnect_serial():
    """Desconecta el puerto serial."""
    global ser, serial_available
    if ser is not None and ser.isOpen():
        try:
            ser.close()
            print("Puerto serial desconectado.")
        except serial.SerialException as e:
            print(f"Error al cerrar el puerto serial: {e}")
    ser = None
    serial_available = False


def disconnect_and_reconnect_serial():
    """Desconecta y reconecta el puerto serial."""
    global temp_values, invalid_line_count
    print("Reconectando el puerto serial...")
    disconnect_serial()
    temp_values = {"D1": None, "D2": None, "D3": None}
    invalid_line_count = 0
    time.sleep(2)
    connect_serial()


def chart_data(request):
    """Obtiene datos del puerto serial y los devuelve en formato JSON."""
    global serial_available, temp_values, invalid_line_count
    data = {
        "time": "",
        "raw_data": [],
        "connected": serial_available
    }

    if serial_available and ser is not None and ser.isOpen():
        try:
            # Intenta leer una línea completa del puerto serial
            try:
                line = ser.readline().decode('utf-8').strip()
            except UnicodeDecodeError as e:
                print(f"Error al decodificar datos: {e}")
                invalid_line_count += 1
                if invalid_line_count >= MAX_INVALID_LINES:
                    disconnect_and_reconnect_serial()
                return JsonResponse(data)

            print(f"Línea recibida: {line}")

            # Validar si la línea contiene un dato válido (D1, D2, D3)
            match = re.match(r'(D[123]):\s*(-?\d+(\.\d+)?)', line)
            if match:
                key, value, _ = match.groups()
                try:
                    temp_values[key] = float(value)
                    invalid_line_count = 0  # Reinicia el contador de errores
                except ValueError:
                    print(f"Valor no numérico para {key}: {value}")
                    invalid_line_count += 1
            else:
                print(f"Línea no válida: {line}")
                invalid_line_count += 1

            # Verifica si ya tenemos los tres valores para enviar datos
            if all(v is not None for v in temp_values.values()):
                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                data.update({
                    "time": time,
                    "raw_data": [temp_values["D1"], temp_values["D2"], temp_values["D3"]]
                })
                # Limpia los valores temporales después de usarlos
                temp_values = {"D1": None, "D2": None, "D3": None}

            # Si se excede el límite de errores, reconecta
            if invalid_line_count >= MAX_INVALID_LINES:
                disconnect_and_reconnect_serial()

        except Exception as e:
            print(f"Error leyendo desde el puerto serial: {e}")
            disconnect_and_reconnect_serial()
    else:
        print("El puerto serial no está disponible o no está conectado.")

    return JsonResponse(data)


def connect_arduino(request):
    """Conecta el Arduino y devuelve el estado."""
    connect_serial()
    return JsonResponse({"connected": serial_available})