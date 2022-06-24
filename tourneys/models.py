from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction
from datetime import datetime
from operator import itemgetter

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

   # find the right car
   def car_index(self, cars, car):
      for i, c in enumerate(cars):
         if c[0].id == car.id:
            return i
      return -1
   
   # gets the results of this tournament
   def results(self):
      races = Race.objects.filter(tourney_id=self.id)
      reg_cars = self.registered_cars.all()
      car_results = []
      for c in reg_cars:
         car_results.append([c, 0, 0])
      for r in races:
         for t in r.trials:
            #[ (car, et, cnt) for car, et, count in cars if car.id  == t.car.id ]
            index = self.car_index(car_results, t.car)
            if index > -1:
               car_results[index][1] += t.et()
               car_results[index][2] += 1
      car_ets = []
      for c in car_results:
         car_ets.append([c[0], c[1]/c[2] if c[2] > 0 else 1000])
      return sorted(car_ets, key=itemgetter(1))

# a single car and the tournament it participates in
class Registration(models.Model):
   tourney = models.ForeignKey(Tournament, on_delete=models.CASCADE)
   car = models.ForeignKey('racers.RaceCar', on_delete=models.CASCADE)

   def __str__(self):
      return f'{self.car} part of {self.tourney}'

# four cars go down the track, 1 winner is a fact
class Race(models.Model):
   tourney = models.ForeignKey(Tournament, on_delete=models.CASCADE)
   start_time = models.BigIntegerField(default=0)
   racers = models.ManyToManyField('racers.RaceCar', through='TimeTrial', related_name='races')
   
   # pretty print this object
   def __str__(self):
      return f'Race {self.id} from {self.tourney}'
      
   # set the time for all lanes of a race
   def set_lane_times(self, times):
      print(f'setting lane times {times}')
      trials = TimeTrial.objects.filter(race_id=self.id).order_by('lane')
      for i, t in enumerate(trials):
         if i < len(times):
            t.end_time = times[i]
            t.save() 
      return

   # set the time for a given lane of this race
   def set_lane_time(self, lane, time):
      trials = TimeTrial.objects.filter(race_id=self.id)
      for t in trials:
         if t.lane == lane:
            t.end_time = time
      return

   # get the start time as a time
   @property
   def time_of_start(self):
      if self.start_time == 0:
         return '?'
      else:
         return timezone.make_aware(datetime.fromtimestamp(self.start_time / (1e9))).time()
   
   # get an elapsed time since the start of the race
   @property
   def et(self):
      if self.start_time:
         return (timezone.now() - self.start_time)
      return -1

   @property
   def trials(self):
      trials = TimeTrial.objects.filter(race_id=self.id).order_by('lane')
      if len(trials) == 4:
         if trials[0].end_time and trials[1].end_time and trials[2].end_time and trials[3].end_time:
            return TimeTrial.objects.filter(race_id=self.id).order_by('end_time')
      return trials

   @property
   def racers_by_lane(self):
      return self.racers.order_by('timetrial__lane')

# a single car and it's time in a single race
class TimeTrial(models.Model):
   MAX_LANES = 4
   race = models.ForeignKey(Race, on_delete=models.CASCADE)
   car = models.ForeignKey('racers.RaceCar', on_delete=models.CASCADE)
   lane = models.IntegerField(validators=[
                                 MaxValueValidator(MAX_LANES),
                                 MinValueValidator(1)
                              ])
   #rank = models.IntegerField(validators=[
   #                              MaxValueValidator(MAX_LANES),
   #                              MinValueValidator(1)
   #                           ])
   mid_time = models.BigIntegerField(default=0)
   end_time = models.BigIntegerField(default=0)
   
   # get the average miles per hour
   def mph(self):
      ftpersec = 40 / self.et()
      return ftpersec * 0.681818
   
   # get the elapsed time at the finish line
   def et(self):
      delta = self.end_time - self.race.start_time
      return delta / 1e9
   
   # pretty print this object
   def __str__(self):
      et = self.et()
      if et > 0:
         return f'[{self.car.id}]{self.car} with ET: {et:.3f}'
      return f'Lane {self.lane}: [{self.car.id}]{self.car}'
