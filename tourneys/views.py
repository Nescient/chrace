from django.shortcuts import get_object_or_404,render
from .models import Race,Tournament,Registration,TimeTrial
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import logging
from django.views.decorators.http import require_http_methods
from django.apps import apps
from django.utils import timezone
from collections import deque

class IndexView(generic.ListView):
   template_name = 'tourneys/index.html'
   context_object_name = 'all'

   def get_queryset(self):
      return Tournament.objects.filter(
         date__lte=timezone.now()
      ).order_by('-date')[:5]

class RaceView(generic.DetailView):
   model = Race
   template_name = 'tourneys/races.html'

@require_http_methods(["GET", "POST"])
def edit(request, pk):
   tourney = get_object_or_404(Tournament, pk=pk)
   my_cars = Registration.objects.filter(tourney_id=tourney.id)#.order_by('name')

   my_cars_ids = []
   for c in my_cars:
      my_cars_ids.append(c.id)

   RaceCar = apps.get_model('racers', 'RaceCar')
   other_cars = RaceCar.objects.exclude(pk__in=my_cars_ids)

   context = {
      'tourney' : tourney,
      'other_cars': other_cars,
      'my_cars' : my_cars,
   }

   return render(request, 'tourneys/edit.html', context)

@require_http_methods(["GET", "POST"])
def run(request, pk):
   tourney = get_object_or_404(Tournament, pk=pk)
   my_cars = tourney.registered_cars.all()
   my_races = Race.objects.filter(tourney_id=tourney.id).order_by('id')
   
   if request.method == 'POST' and not my_races:
      # create new races based on registered cars
      print('creating new races')
      lanes = [ deque(), deque(), deque(), deque() ]
      for c in my_cars:
         for a in lanes:
            a.append(c)
      for i,a in enumerate(lanes):
         a.rotate(i)
      while len(lanes[0]) > 0 or len(lanes[1]) > 0 or len(lanes[2]) > 0 or len(lanes[3]) > 0:
         race = Race.objects.create(tourney=tourney)
         for i,a in enumerate(lanes):
            #race.racers.add(a[0], lane=i+1)
            #SauceQuantity.objects.create(sandwich=chicken_teriyaki_sandwich, sauce=bbq_sauce, extra_sauce=True)
            if len(a) > 0:
               #race.racers.add(TimeTrial.objects.create(race=race,car=a[0],lane=i+1))
               #tt = race.racers.add(a[0], lane=i+1)
               #tt.lane = i + 1
               TimeTrial.objects.create(race=race,car=a[0],lane=i+1)
               a.popleft()
         race = Race.objects.get(id=race.id)
         print(race.racers.all())
      my_races = Race.objects.filter(tourney_id=tourney.id).order_by('id')

   my_cars_ids = []
   for c in my_cars:
      my_cars_ids.append(c.id)

   RaceCar = apps.get_model('racers', 'RaceCar')
   other_cars = RaceCar.objects.exclude(pk__in=my_cars_ids)

   if request.method == 'POST':
      # get ready to rumble
      print('go')
      for r in my_races:
         print(r)
         print(r.racers)
         if not r.start_time:
            import os
            os.system(f'python3 /home/pi/chrace/gpio.py {r.id} &')
            break

   context = {
      'tourney' : tourney,
      'my_cars' : my_cars,
      'my_races' : my_races,
   }

   return render(request, 'tourneys/run.html', context)
