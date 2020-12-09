from django.urls import path
from . import views

app_name : 'index'
urlpatterns = [
    path('index/', views.index, name="index"),  
    path('time/', views.time, name="time"),
    path('fare/', views.fare, name="fare"),
    path('center/', views.center, name="center"),
    path('way/', views.way, name="way"),
    path('facility/', views.facility, name="facility"),
    path('kids/time/', views.kids_time, name='kidsTime'),
    path('kids/fare/', views.kids_fare, name='kidsFare'),
    path('elite/time/', views.elite_time, name='eliteTime'),
    path('elite/fare/', views.elite_fare, name='eliteFare')
]