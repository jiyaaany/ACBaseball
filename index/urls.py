from django.urls import path
from . import views

app_name : 'index'
urlpatterns = [
    path('index/', views.index, name="index"),  
    path('time/', views.time, name="time"),
    path('fare/', views.fare, name="fare"),
]