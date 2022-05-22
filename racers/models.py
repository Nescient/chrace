from django.db import models

# this represents the human "driving" the car
class Driver(models.Model):
   first_name = models.CharField(max_length=32)
   last_name = models.CharField(max_length=32)
   birthday = models.DateField()

# this represents a single created car
class RaceCar(models.Model):
   driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
   name = models.CharField(max_length=64)
