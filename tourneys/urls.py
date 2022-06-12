from django.urls import path

from . import views

app_name = 'tourneyz'
urlpatterns = [
   path('', views.IndexView.as_view(), name='index'),
   path('<int:pk>/races/', views.RaceView.as_view(), name='races'),
   path('<int:pk>/', views.edit, name='edit'),
   path('<int:pk>/go', views.TourneyRunView.as_view(), name='run'),
]