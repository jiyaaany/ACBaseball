from django.urls import path
from . import views

app_name = 'schedule'
urlpatterns = [
    path('', views.show_schedule, name='show_schedule'),
    path('show_schedule/', views.show_schedule, name='show_schedule'),
    path('book_schedule/', views.book_schedule, name='book_schedule'),
    path('schedule_form/', views.schedule_form, name='schedule_form'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('schedule_detail/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    path('cancel_schedule/<int:pk>/', views.cancel_schedule, name='cancel_schedule')
]