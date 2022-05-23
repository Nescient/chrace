from django.shortcuts import get_object_or_404,render
from .models import Driver,RaceCar

def index(request):
   all_cars = RaceCar.objects.all()
   context = {'all_cars': all_cars}
   return render(request, 'racers/index.html', context)

def races(request, driver_id):
   driver = get_object_or_404(Driver, pk=driver_id)
   return render(request, 'racers/races.html', {'driver': driver})

def times(request, car_id):
   car = get_object_or_404(RaceCar, pk=car_id)
   return render(request, 'racers/times.html', {'car': car})
