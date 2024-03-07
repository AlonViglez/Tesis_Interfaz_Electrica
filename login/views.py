from django.shortcuts import render

from django.http import HttpResponse

# Create your tests here.
def hello(request):
    return HttpResponse("Helloiu")
