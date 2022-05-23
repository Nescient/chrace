from django.db import models
from django.utils import timezone

# this represents the human "driving" the car
class Driver(models.Model):
   first_name = models.CharField(max_length=32)
   last_name = models.CharField(max_length=32)
   birthday = models.DateField()

   # the driver's age (as of today)
   def age(self):
      today = timezone.now()
      dob = self.birthday
      years = today.year - dob.year
      if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
        years -= 1
      return years


   # a better way to represent drivers
   def __str__(self):
      age = self.age()
      agestr = f'{self.age()}yo'
      if age > 17:
         agestr = 'Adult'
      elif age > 12:
         agestr = 'Teen'
      return f'{self.first_name.capitalize()} {self.last_name.capitalize()} ({agestr})'

# this represents a single created car
class RaceCar(models.Model):
   driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
   name = models.CharField(max_length=64)

   def __str__(self):
      return self.name
