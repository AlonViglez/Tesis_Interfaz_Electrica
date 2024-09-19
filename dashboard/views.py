from django.shortcuts import render,redirect
from login.models import Usuario,Maestro
from django.http import HttpResponse
from django.http import JsonResponse
import serial
import re
import random
import datetime
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
            return render(request, template_name, {'usuario': usuario, 'datos': datos}) #Enviar al html junto con los datos
        
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
ser = None #Variable serial None para que no haya una conexion serial activa
serial_available = False #Estado del serial en falso 

def connect_serial():
    global ser, serial_available  # Variables globales ser y serial_available para permitir su modificación dentro de la función.
    try:
        if ser is None or not ser.isOpen():  # Verifica si no hay una conexión activa o si el puerto no está abierto.
            ser = serial.Serial('COM5', 9600)  # Abrir una conexión en el puerto 'COM5' con una tasa de 9600 baudios.
            serial_available = True  # Marca el estado del serial conectado con éxito.
    except serial.SerialException as e:  #Capturar alguna excepción relacionada con el puerto.
        print(f"Error opening serial port: {e}") 
        ser = None  # Reinicia ser a None en caso de fallo para evitar usar una conexión errónea.
        serial_available = False  # Marca el serial como no disponible si no se pudo conectar.

def disconnect_serial():
    global ser, serial_available  # Nuevamente, se usan las variables globales para permitir su modificación.
    if ser is not None and ser.isOpen():  # Verifica si el serial está conectado y abierto antes de intentar cerrarlo.
        try:
            ser.close()  # Intenta cerrar la conexión serial.
        except serial.SerialException as e:  # Captura cualquier error relacionado con el cierre del puerto.
            print(f"Error closing serial port: {e}") 
        finally:
            ser = None  # Reinicia ser a None tras cerrar la conexión, ya sea exitoso o con error.
            serial_available = False  # Marca el serial como no disponible tras el cierre.

def extract_temperature(line):
    match = re.search(r'Temperatura: (\d+\.\d+)', line) #Busca una cadena de texto que comience con "Temperatura: " seguida de un número decimal
    
    if match: 
        temperature = float(match.group(1))  # Extrae el valor numérico de la coincidencia y lo convierte a float.
        return temperature  # Devolver el valor de temperatura
    
    return None  #Si no se encuentra ninguna coincidencia, devuelve None.

def extract_voltage(line):
    match = re.search(r'Voltaje: (\d+\.\d+)', line) #Busca una cadena de texto que comience con "Voltaje: " seguida de un número decimal
    
    if match: 
        voltage = float(match.group(1))  # Extrae el valor numérico de la coincidencia y lo convierte a float.
        return voltage  # Devolver el valor de voltaje
    
    return None  # Si no se encuentra ninguna coincidencia, devuelve None.

def chart_data(request):
    #Inicializa un diccionario con datos predeterminados
    data = {
        "time": "",
        "temperature": None,
        "voltage": None,
        "connected": serial_available
    }
    #Verifica si la conexión serial está disponible y si el puerto está abierto.
    if serial_available and ser.isOpen():
        try:
            #Lee una línea de datos desde el puerto serial, decodifica en UTF-8 y elimina los espacios en blanco.
            line = ser.readline().decode('utf-8').strip()

            # Extrae la temperatura y el voltaje de la línea de datos utilizando las funciones definidas.
            temperature = extract_temperature(line)
            voltage = extract_voltage(line)
            
            if 'numero_cuenta' in request.session:
                numero_cuenta = request.session['numero_cuenta'] #Obtener el numero de cuenta del alumno
                #Si existen valores válidos para temperatura y voltaje se hace lo siguiente
                if temperature is not None and voltage is not None:
                    #Obtiene la fecha y hora actuales en formato ISO 8601.
                    now = datetime.datetime.now()
                    time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

                    # Almacenar los datos en la base de datos
                    DatosAlumno.objects.create(
                        voltaje=voltage,
                        temperatura=temperature,
                        fecha=now,  
                        id_alumno=numero_cuenta  # Guarda el numero_cuenta en el campo id_alumno
                    )

                    #Actualiza el diccionario 'data' con los valores de tiempo, temperatura y voltaje.
                    data.update({
                        "time": time,
                        "temperature": temperature,
                        "voltage": voltage
                    })

        except Exception as e:
            # Imprime un mensaje de error si ocurre una excepción al leer del puerto serial.
            print(f"Error reading from serial port: {e}")
            # Desconecta el puerto serial en caso de error
            disconnect_serial()
    #Devuelve los datos en formato JSON como respuesta.
    return JsonResponse(data)

def connect_arduino(request):
    connect_serial() #Ir a la función de conectar serial
    return JsonResponse({"connected": serial_available}) # Devuelve una respuesta JSON que indica si la conexión serial está disponible (True) o no (False).