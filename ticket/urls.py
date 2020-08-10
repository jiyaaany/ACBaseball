from django.urls import path
from . import views

app_name = 'ticket'
urlpatterns = [
    path('form/', views.form, name='form'),
    path('create/', views.create, name='create'),
    
]