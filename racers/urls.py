from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:driver_id>/races/', views.races, name='races'),
    path('<int:car_id>/times/', views.times, name='times'),
]