from django.shortcuts import get_object_or_404,render
from .models import Race,Tournament
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
   template_name = 'tourneys/index.html'
   context_object_name = 'all'

   def get_queryset(self):
      return Tournament.objects.all()

class DetailView(generic.DetailView):
   model = Race
   template_name = 'tourneys/races.html'

class ResultsView(generic.DetailView):
   model = Tournament
   template_name = 'tourneys/tourney.html'

def index(request):
   all = Tournament.objects.all()
   context = {'all': all}
   return render(request, 'tourneys/index.html', context)

def races(request, race_id):
   model = get_object_or_404(Race, pk=race_id)
   return render(request, 'tourneys/races.html', {'race': model})

def tourney(request, tourney_id):
   model = get_object_or_404(Tournament, pk=tourney_id)
   return render(request, 'tourneys/tourney.html', {'tourney': model})
