"""hacer uso el metodo """
from django.http import HttpResponse 
from django.shortcuts import render 

def simple(request):
    return render(request,'simple.html', { })