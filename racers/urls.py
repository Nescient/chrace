from django.urls import path

from . import views

app_name = 'drivers'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:driver_id>/races/', views.races, name='races'),
    path('<int:car_id>/times/', views.times, name='times'),
]