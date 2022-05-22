from django.db import models


class Driver(models.Model):
   first_name = models.CharField(max_length=32)
   last_name = models.CharField(max_length=32)
   birthday = models.DateField()

class RaceCar(models.Model):
   driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
   name = models.CharField(max_length=64)
   votes = models.IntegerField(default=0)

class Tournament(models.Model):
   date = models.DateField()
   first = models.ForeignKey(Driver, on_delete=models.CASCADE)
   second = models.ForeignKey(Driver, on_delete=models.CASCADE)
   third = models.ForeignKey(Driver, on_delete=models.CASCADE)

class Race(models.Model):
   tourney = models.ForeignKey(Tournament, on_delete=models.CASCADE)
   start_time = models.DateTimeField()
   racers = models.ManyToManyField(RaceCar, through='TimeTrial')

class TimeTrial(models.Model):
   race = models.ForeignKey(Race, on_delete=models.CASCADE)
   car = models.ForeignKey(RaceCar, on_delete=models.CASCADE)
   mid_time_ns = models.IntegerField()
   end_time_ns = models.IntegerField()

