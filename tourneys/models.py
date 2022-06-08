from django.db import models
from django.utils import timezone

# get our racers models
from django.apps import apps
# Driver = apps.get_model('racers', 'Driver')
# RaceCar = apps.get_model('racers', 'RaceCar')

# this represents a set of races
class Tournament(models.Model):
   date = models.DateField()
   #first = models.ForeignKey('racers.Driver', on_delete=models.CASCADE)
   #second = models.ForeignKey('racers.Driver', on_delete=models.CASCADE)
   #third = models.ForeignKey('racers.Driver', on_delete=models.CASCADE)
   
   def first(self):
      return 0

# four cars go down the track, 1 winner is a fact
class Race(models.Model):
   tourney = models.ForeignKey(Tournament, on_delete=models.CASCADE)
   start_time = models.DateTimeField()
   racers = models.ManyToManyField('racers.RaceCar', through='TimeTrial')

# a single car and it's time in a single race
class TimeTrial(models.Model):
   race = models.ForeignKey(Race, on_delete=models.CASCADE)
   car = models.ForeignKey('racers.RaceCar', on_delete=models.CASCADE)
   #mid_time_ns = models.IntegerField()
   #end_time_ns = models.IntegerField()
   end_time = models.DateTimeField()
   
   # get the average miles per hour
   def mph(self):
      ftpersec = 40 / self.et()
      return ftpersec * 0.681818
   
   # get the elapsed time at the finish line
   def et(self):
      delta = self.race.start_time - self.end_time
      return delta.total_seconds()
   
   def __str__(self):
      return f'{self.car} with ET: {self.et():.3f}'
