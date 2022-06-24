from django.shortcuts import get_object_or_404,render
from .models import Race,Tournament,Registration,TimeTrial
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import logging
from django.views.decorators.http import require_http_methods
from django.apps import apps
from django.utils import timezone
from collections import deque
import json

MAX_LANES = 4

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
   my_cars = tourney.registered_cars.all()

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
   live_race = next_race = tourney_results = None
   
   if request.method == 'POST' and not my_races:
      # create new races based on registered cars
      print('creating new races')
      lanes = [ deque(), deque(), deque(), deque() ]
      for c in my_cars:
         for a in lanes:
            a.append(c)
      for i,a in enumerate(lanes):
         while len(a) < MAX_LANES:
            a.append(None)
         a.rotate(i)
      print(lanes)
      while len(lanes[0]) > 0 or len(lanes[1]) > 0 or len(lanes[2]) > 0 or len(lanes[3]) > 0:
         race = Race.objects.create(tourney=tourney)
         for i,a in enumerate(lanes):
            if len(a) > 0:
               if a[0]:
                  TimeTrial.objects.create(race=race,car=a[0],lane=i+1)
               a.popleft()
      my_races = Race.objects.filter(tourney_id=tourney.id).order_by('id')

   if request.GET.get('startracebtn') and request.GET.get('raceid'):
      # get ready to rumble
      raceid = request.GET.get('raceid')
      live_race = int(raceid)
      print(f'Starting Race {raceid}')
      import os
      os.system(f'python3 /home/pi/chrace/gpio.py {raceid} &')
   else:
       for r in my_races:
          if not r.start_time:
             next_race = r.id
             break

   if not next_race:
      tourney_results = tourney.results()
   
   context = {
      'tourney' : tourney,
      'my_cars' : my_cars,
      'my_races' : my_races,
      'live_race' : live_race,
      'next_race' : next_race,
      'results' : tourney_results
   }

   return render(request, 'tourneys/run.html', context)

def race_result(request):
   # request.is_ajax() is deprecated since django 3.1
   is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
   print(f'is ajax {is_ajax}')
   if is_ajax:
      if request.method == 'POST':
         data = json.load(request)
         raceid = data.get('raceid')
         race = get_object_or_404(Race, pk=raceid)
         trials = TimeTrial.objects.filter(race_id=race.id).order_by('lane')
         context = {
            'start_time' : race.start_time,
            #'lane1' : trials[0].et() if len(trials) > 0 else 0,
            #'lane2' : trials[1].et() if len(trials) > 1 else 0,
            #'lane3' : trials[2].et() if len(trials) > 2 else 0,
            #'lane4' : trials[3].et() if len(trials) > 3 else 0,
         }
         return JsonResponse(context)
      return JsonResponse({'status': 'Invalid request'}, status=400)
   else:
      return HttpResponseBadRequest('Invalid request')
