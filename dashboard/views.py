from django.shortcuts import render,redirect
from login.models import Usuario,Maestro
from django.http import HttpResponse
from django.http import JsonResponse
import serial
import re
import random
import datetime
import time
import json
from .models import BotonEstado
from . forms import Maestrocitar
from .models import DatosAlumno,SensorData  # Modelo de la tabla alumnos
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
            #datos = DatosAlumno.objects.filter(id_alumno=usuario.numero_cuenta) #Filtrar datos del alumno por su numero de cuenta
            datos = DatosAlumno.objects.all()
            return render(request, template_name, {'usuario': usuario, 'datos': datos}) #Enviar al html junto con ambos datos
        
        return render(request, template_name, {'usuario': usuario}) #Enviar al html solo los datos del usuario
    else:
        return redirect('home')
#Checar si esta logueado el maestro sino mandarlo al home
def check_logueado_Maestro(request, template_name, filtrar_datos=False):
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = Maestro.objects.get(id=usuario_id)
        # Guardar numero_cuenta en la sesión que se usará para identificar quien esta guardando los datos
        request.session['email'] = usuario.email
        if filtrar_datos:
            datos = DatosAlumno.objects.all()
            return render(request, template_name, {'usuario': usuario, 'datos': datos}) #Enviar al html junto con ambos datos
        
        return render(request, template_name, {'usuario': usuario}) #Enviar al html solo los datos del usuario
    else:
        return redirect('home')
#Registro maestro
def agendar_fecha_view(request):
    if request.method == 'POST':
        form = Maestrocitar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grafpulsoM')  # Redirigir a una página de éxito
    else:
        form = Maestrocitar()
    return render(request, 'agendar_fecha.html', {'form': form})
#Seccion del alumno

def grafpulso(request):
    return check_logueado(request, 'grafica_de_pulso.html')

def graflineal(request):
    return check_logueado(request, 'grafica_lineal.html')

def grafbarra(request):
    return check_logueado(request, 'grafbarra.html')

#Seccion Maestros
def grafagendar(request):
    return check_logueado(request, 'agendar.html')

def grafpulsoM(request):
    return check_logueado_Maestro(request, 'grafica_de_pulsoM.html')

def graflinealM(request):
    return check_logueado_Maestro(request, 'grafica_linealM.html')

def grafbarraM(request):
    return check_logueado_Maestro(request, 'grafbarraM.html')

def solicitudes(request):
    return check_logueado_Maestro(request, 'solicitudes.html')

def historial_view(request):
    return check_logueado(request, 'historial_graficas.html', filtrar_datos=True)

def historial_view_maestro(request):
    return check_logueado_Maestro(request, 'historial_graficasM.html', filtrar_datos=True)

def chart(request):
    return check_logueado(request, 'simplechart.py')

# Variables globales para el puerto serial
ser = None
serial_available = False

# Variables auxiliares
temp_values = {"D1": None, "D2": None, "D3": None}
invalid_line_count = 0
MAX_INVALID_LINES = 3
RECONNECT_DELAY = 1  # Segundos de espera antes de reintentar conexión
MAX_RECORDS = 25  # Límite de registros en la base de datos

def connect_serial():
    """Conecta al puerto serial."""
    global ser, serial_available
    try:
        if ser is None or not ser.isOpen():
            ser = serial.Serial('COM5', 9600, timeout=1)
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
    """Desconecta y reconecta el puerto serial después de un retraso."""
    global ser, serial_available
    disconnect_serial()
    print("Reintentando conexión con el puerto serial en breve...")
    time.sleep(RECONNECT_DELAY)  # Espera antes de reconectar
    connect_serial()

def chart_data(request):
    """Lee datos del puerto serial y almacena en la base de datos."""
    global serial_available, temp_values, invalid_line_count
    # Obtener el parámetro storeData desde la URL
    should_store_data = request.GET.get('storeData', 'false').lower() == 'true'
    data = {
        "time": "",
        "raw_data": [],
        "connected": serial_available,
    }

    if serial_available and ser is not None and ser.isOpen():
        try:
            # Leer línea desde el puerto serial
            line = ser.readline().decode('utf-8').strip()
            print(f"Línea recibida: {line}")

            # Validar el formato de la línea
            match = re.match(r'(D[123]):\s*(-?\d+(\.\d+)?)', line)
            if match:
                key, value, _ = match.groups()
                temp_values[key] = float(value)
                print(f"Actualizado {key} con valor: {value}")
                invalid_line_count = 0

                # Verificar si todos los datos han sido recibidos
                if all(temp_values[key] is not None for key in temp_values):
                    # Guardar datos en la base de datos
                    SensorData.objects.create(
                        d1=temp_values["D1"],
                        d2=temp_values["D2"],
                        d3=temp_values["D3"],
                    )

                    if should_store_data:
                        DatosAlumno.objects.create(
                            d1=temp_values["D1"],
                            d2=temp_values["D2"],
                            d3=temp_values["D3"],
                        )

                    # Reiniciar los valores
                    temp_values = {"D1": None, "D2": None, "D3": None}

                    # Comprobar y eliminar registros si hay más de 5
                    if SensorData.objects.count() > MAX_RECORDS:
                        SensorData.objects.all().delete()  # Eliminar todos los registros

            else:
                invalid_line_count += 1
                print(f"Línea inválida: {line}")

            # Desconectar si hay demasiadas líneas inválidas
            if invalid_line_count >= MAX_INVALID_LINES:
                print("Demasiadas líneas inválidas. Desconectando y reconectando...")
                disconnect_and_reconnect_serial()

        except Exception as e:
            print(f"Error leyendo desde el puerto serial: {e}")
            disconnect_and_reconnect_serial()

    else:
        # Si no está conectado, intenta reconectar
        print("Puerto serial no disponible. Intentando reconectar...")
        disconnect_and_reconnect_serial()

    # Consultar los últimos datos de la base de datos
    latest_data = SensorData.objects.order_by('-timestamp').first()
    if latest_data:
        data.update({
            "time": latest_data.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "raw_data": [latest_data.d1, latest_data.d2, latest_data.d3],
        })

    print(data)
    return JsonResponse(data)

def db_data(request):
    # Consulta los últimos datos de la base de datos
    data = {
        "time": "",
        "raw_data": [],
        "connected": serial_available,
    }

    latest_data = SensorData.objects.order_by('-timestamp').first()
    if latest_data:
        data.update({
            "time": latest_data.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "raw_data": [latest_data.d1, latest_data.d2, latest_data.d3],
        })
    else:
        print("No se encontraron datos en la base de datos.")

    print(data)  # Imprime los datos que se devolverán
    return JsonResponse(data)

def connect_arduino(request):
    """Conecta el Arduino y devuelve el estado."""
    connect_serial()
    return JsonResponse({"connected": serial_available})


def obtener_estado_boton(request):
    """Obtiene el estado del botón."""
    try:
        boton = BotonEstado.objects.first()
        if not boton:
            boton = BotonEstado.objects.create(estado=False)
        return JsonResponse({'estado': boton.estado})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def actualizar_estado_boton(request):
    """Actualiza el estado del botón."""
    if request.method == 'POST':
        try:
            estado_boton = request.POST.get('estado') == 'true'

            # Actualizar el modelo BotonEstado en la base de datos
            boton, _ = BotonEstado.objects.get_or_create(id=1)
            boton.estado = estado_boton
            boton.save()

            return JsonResponse({'estado': estado_boton})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
