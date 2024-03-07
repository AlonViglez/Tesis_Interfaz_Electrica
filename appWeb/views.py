"""hacer uso el metodo """
from django.http import HttpResponse 
def saludo(request):
    return HttpResponse("Hola mundo")

def despedida(request):
    return HttpResponse("Nos vemos")


#recepcionando parametro (edad)
def adulto(request, edad):
    if edad >= 18:
        return HttpResponse("Eres mayor de edad, puedes acceder")
    else:
        return HttpResponse("Eres menor de edad, no puedes acceder")