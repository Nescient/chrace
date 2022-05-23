# from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Driver,RaceCar

def index(request):
   latest_tourney = RaceCar.objects.all()
   context = {'latest_tourney': latest_tourney}
   return render(request, 'racers/index.html', context)

def races(request, driver_id):
   try:
      driver = Driver.objects.get(pk=driver_id)
   except Driver.DoesNotExist:
      raise Http404(f'Driver {driver_id} does not exist')
   return render(request, 'racers/races.html', {'driver': driver})

def times(request, car_id):
   try:
      car = RaceCar.objects.get(pk=car_id)
      #driver = Driver.objects.get(pk=car.driver)
   except RaceCar.DoesNotExist:
      raise Http404(f'Car {car_id} does not exist')
   return render(request, 'racers/times.html', {'car': car, 'driver': 'sam'})
