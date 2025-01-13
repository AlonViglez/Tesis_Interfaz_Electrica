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
import openpyxl
from .models import BotonEstado
from . forms import Maestrocitar
from .models import DatosAlumno,SensorData  # Modelo de la tabla alumnos
from django.views.decorators.csrf import csrf_exempt
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

def obtener_dato_reciente(request):
    try:
        # Verificar el estado del botón
        boton_estado = BotonEstado.objects.first()  # Suponemos un solo registro
        if not boton_estado or not boton_estado.estado:
            return JsonResponse({"error": "El botón no está activado. No hay datos nuevos."})

        # Obtener el dato más reciente
        dato_reciente = DatosAlumno.objects.latest('fecha')
        data = {
            "fecha": dato_reciente.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "d1": dato_reciente.d1,
            "d2": dato_reciente.d2,
            "d3": dato_reciente.d3,
        }
    except DatosAlumno.DoesNotExist:
        data = {
            "error": "No hay datos disponibles."
        }
    return JsonResponse(data)

def export_to_excel(request):
    # Crear un libro de Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sensor Data"

    # Agregar encabezados
    headers = ['ID', 'D1', 'D2', 'D3']
    sheet.append(headers)

    # Agregar datos de la tabla 'dashboard_sensordata'
    data = DatosAlumno.objects.all()
    for item in data:
        sheet.append([item.id, item.d1, item.d2, item.d3])

    # Configurar respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=sensordata.xlsx'
    workbook.save(response)

    return response

@csrf_exempt
def update_botonestado(request):
    if request.method == 'POST':
        try:
            # Leer los datos enviados por la solicitud
            data = json.loads(request.body)
            activo = data.get('activo', False)

            # Actualizar o crear el estado en la base de datos
            boton, created = BotonEstado.objects.update_or_create(
                id=1,  # Asegúrate de usar un identificador único o lógica apropiada
                defaults={'estado': activo}
            )

            return JsonResponse({'success': True, 'estado': boton.estado})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})