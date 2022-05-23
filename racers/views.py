# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import RaceCar

def index(request):
   latest_tourney = RaceCar.objects.all()
   output = ', '.join([c.name for c in latest_tourney])
   return HttpResponse(output)

def races(request, driver_id):
    return HttpResponse(f'This is the list of all races for Driver {driver_id}.')

def times(request, car_id):
    return HttpResponse(f'This is the list of all races for Car {car_id}.')