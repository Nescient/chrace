from django.contrib import admin

from .models import Race, TimeTrial, Tournament

admin.site.register(Race)
admin.site.register(TimeTrial)
admin.site.register(Tournament)