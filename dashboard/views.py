from django.shortcuts import render,redirect
from login.models import Usuario,Maestro
from django.http import HttpResponse
from django.http import JsonResponse
import serial
import re
import random
import datetime


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
    return check_logueado_Maestro(request, 'solicitudes.html')

#Código para ARDUINO NANO, sensor LM35 
ser = serial.Serial('COM7', 9600)

def extract_temperature(line):
    # Utiliza una expresión regular para buscar el número flotante que representa la temperatura
    match = re.search(r'Temperatura: (\d+\.\d+)', line)
    if match:
        temperature = float(match.group(1))
        return temperature
    return None

def extract_voltage(line):
    # Utiliza una expresión regular para buscar el número flotante que representa el voltaje
    match = re.search(r'Voltaje: (\d+\.\d+)', line)
    if match:
        voltage = float(match.group(1))
        return voltage
    return None

def chart_data(request):
    try:
        if ser.isOpen():
            line = ser.readline().decode('utf-8').strip()
            temperature = extract_temperature(line)
            voltage = extract_voltage(line)
            if temperature is not None and voltage is not None:
                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

                data = {
                    "time": time,
                    "temperature": temperature,
                    "voltage": voltage
                }
                return JsonResponse(data)
    except Exception as e:
        print("Error reading from serial port: " + str(e))
    
    # Si hay un error o no se puede abrir el puerto serial, se envía un valor de temperatura y voltaje nulos
    return JsonResponse({"time": "", "temperature": None, "voltage": None})
