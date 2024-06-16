from django.shortcuts import render,redirect
from login.models import Usuario,Maestro
from django.http import HttpResponse
from django.http import JsonResponse
import serial
import re
import random
import datetime
from . forms import Maestrocitar
#from . forms import registrarAgenda #Uso de mi formulario


#Checar si esta logueado el alumno sino mandarlo al home
def check_logueado(request, template_name):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Usuario.objects.get(id=usuario_id)
        return render(request, template_name,{'usuario': usuario})
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

def chart(request):
    return check_logueado(request, 'simplechart.py')

# Variables globales para el puerto serial
ser = None
serial_available = False

def connect_serial():
    global ser, serial_available
    try:
        if ser is None or not ser.isOpen():
            ser = serial.Serial('COM7', 9600)
            serial_available = True
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        ser = None
        serial_available = False

def disconnect_serial():
    global ser, serial_available
    if ser is not None and ser.isOpen():
        try:
            ser.close()
        except serial.SerialException as e:
            print(f"Error closing serial port: {e}")
        finally:
            ser = None
            serial_available = False

def extract_temperature(line):
    match = re.search(r'Temperatura: (\d+\.\d+)', line)
    if match:
        temperature = float(match.group(1))
        return temperature
    return None

def extract_voltage(line):
    match = re.search(r'Voltaje: (\d+\.\d+)', line)
    if match:
        voltage = float(match.group(1))
        return voltage
    return None

def chart_data(request):
    data = {"time": "", "temperature": None, "voltage": None, "connected": serial_available}
    if serial_available and ser.isOpen():
        try:
            line = ser.readline().decode('utf-8').strip()
            temperature = extract_temperature(line)
            voltage = extract_voltage(line)
            if temperature is not None and voltage is not None:
                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

                data.update({
                    "time": time,
                    "temperature": temperature,
                    "voltage": voltage
                })
        except Exception as e:
            print(f"Error reading from serial port: {e}")
            disconnect_serial()
    return JsonResponse(data)

def connect_arduino(request):
    connect_serial()
    return JsonResponse({"connected": serial_available})