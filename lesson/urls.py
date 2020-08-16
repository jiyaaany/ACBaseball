from django.urls import path
from . import views
from django.urls import re_path


app_name = 'lesson'
urlpatterns = [
    path('form/', views.form, name='form'),
    path('list/', views.list, name='list'),
    # re_path(r'^list/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})$', views.list, name='list')
    # path('list/<date:date>', views.list, name='list'),
    
]

# ^(?P<date>\d{4}-\d{2}-\d{2})/$