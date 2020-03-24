from django.shortcuts import render
from django.http import JsonResponse
from web import models
import pickle

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')