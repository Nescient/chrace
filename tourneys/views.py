from django.shortcuts import get_object_or_404,render
from .models import Race,Tournament
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import logging
from django.views.decorators.http import require_http_methods
from django.apps import apps

class IndexView(generic.ListView):
   template_name = 'tourneys/index.html'
   context_object_name = 'all'

   def get_queryset(self):
      return Tournament.objects.all()

class RaceView(generic.DetailView):
   model = Race
   template_name = 'tourneys/races.html'

@require_http_methods(["GET", "POST"])
def edit(request, pk):
   tourney = get_object_or_404(Tournament)
   RaceCar = apps.get_model('racers', 'RaceCar')
   all_cars = RaceCar.objects.all()
   context = {
      'tourney' : tourney,
      'all_cars': all_cars,
   }
   return render(request, 'tourneys/edit.html', context)

class TourneyEditView(generic.DetailView):
   model = Tournament
   template_name = 'tourneys/edit.html'
   
   def get_all_cars(self):
      RaceCar = apps.get_model('racers', 'RaceCar')
      return RaceCar.objects.all()

class TourneyRunView(generic.DetailView):
   model = Tournament
   template_name = 'tourneys/run.html'

def index(request):
   latest_tourney_list = Tournament.objects.order_by('-date')[:5]
   context = {'latest_tourney_list': latest_tourney_list}
   return render(request, 'tourneys/index.html', context)