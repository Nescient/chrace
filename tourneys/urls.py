from django.urls import path

from . import views

app_name = 'tourneyz'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/races/', views.DetailView.as_view(), name='races'),
    path('<int:pk>/', views.ResultsView.as_view(), name='tourney'),
]