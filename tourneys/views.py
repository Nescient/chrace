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
   my_cars = Registration.objects.filter(tourney_id=tourney.id)
   my_races = Race.objects.filter(tourney_id=tourney.id)
   
   if request.method == 'POST' and not my_races:
      # create new races based on registered cars
      print('go')

   my_cars_ids = []
   for c in my_cars:
      my_cars_ids.append(c.id)

   RaceCar = apps.get_model('racers', 'RaceCar')
   other_cars = RaceCar.objects.exclude(pk__in=my_cars_ids)

   if request.method == 'POST':
      # get ready to rumble
      print('go')

   context = {
      'tourney' : tourney,
      'my_cars' : my_cars,
      'my_races' : my_races,
   }

   return render(request, 'tourneys/run.html', context)
