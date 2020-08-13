from django.urls import path
from . import views

app_name = 'ticket'
urlpatterns = [
    path('form/', views.form, name='form'),
    path('create/', views.create, name='create'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('list/', views.list, name='list'),
]