from django.urls import path
from . import views
from django.urls import re_path


app_name = 'lesson'
urlpatterns = [
    path('form/', views.form, name='form'),
    path('list/', views.list, name='list'),
    path('apply/<int:id>', views.apply, name='apply'),
    path('photo/', views.photo, name='photo'),
    path('movie/', views.movie, name='movie'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('get/<slug:date>', views.get, name='get'),
]