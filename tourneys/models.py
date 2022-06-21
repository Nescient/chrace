from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction

# this represents a set of races and register cars
class Tournament(models.Model):
   # the date of the tournament
   date = models.DateField()
   
   # the registered cars for the tournament
   registered_cars = models.ManyToManyField('racers.RaceCar', through='Registration')
   
   # only one tournament can be active at a time
   active = models.BooleanField(default=False)

   # the pretty print string for this object   
   def __str__(self):
      return f'Tournament {self.id} on {self.date}'
   
   # sets this tournament as active
   @transaction.atomic
   def activate(self):
      if not self.active:
         self.active = True
         return True
      return False

   # sets this tournament as inactive
   @transaction.atomic
   def deactivate(self):
      if self.active:
         self.active = False
         return True
      return False
   
   # gets the results of this tournament
   def results(self):
      return 0

# a single car and the tournament it participates in
class Registration(models.Model):
   tourney = models.ForeignKey(Tournament, on_delete=models.CASCADE)
   car = models.ForeignKey('racers.RaceCar', on_delete=models.CASCADE)

   def __str__(self):
      return f'{self.car} part of {self.tourney}'

# four cars go down the track, 1 winner is a fact
class Race(models.Model):
   tourney = models.ForeignKey(Tournament, on_delete=models.CASCADE)
   start_time = models.TimeField(null=True, blank=True)
   racers = models.ManyToManyField('racers.RaceCar', through='TimeTrial')
   
   # pretty print this object
   def __str__(self):
      return f'Race {self.id} from {self.tourney}'

   # set the time for a given lane of this race
   def set_lane_time(self, lane, time):
      trials = TimeTrial.objects.filter(race_id=self.id)
      for t in trials:
         if t.lane == lane:
            t.end_time = time

# a single car and it's time in a single race
class TimeTrial(models.Model):
   MAX_LANES = 4
   race = models.ForeignKey(Race, on_delete=models.CASCADE)
   car = models.ForeignKey('racers.RaceCar', on_delete=models.CASCADE)
   lane = models.IntegerField(validators=[
                                 MaxValueValidator(MAX_LANES),
                                 MinValueValidator(1)
                              ])
   mid_time = models.TimeField(null=True, blank=True)
   end_time = models.TimeField(null=True, blank=True)
   
   # get the average miles per hour
   def mph(self):
      ftpersec = 40 / self.et()
      return ftpersec * 0.681818
   
   # get the elapsed time at the finish line
   def et(self):
      if not self.race.start_time or not self.end_time:
         return -1
      delta = self.race.start_time - self.end_time
      return delta.total_seconds()
   
   # pretty print this object
   def __str__(self):
      et = self.et()
      et_str = '{self.et():.3f}' if et >= 0 else '?'
      return f'{self.car} with ET: {et_str}'
