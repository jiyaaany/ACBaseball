from django.urls import path
from . import views

app_name = 'cafe'
urlpatterns = [
    path('form/', views.form, name='form'),
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('detail/', views.detail, name='detail'),
    path('photo/', views.photo, name="baseball_photo"),
    path('movie/', views.movie, name="baseball_movie"),
    path('photo_form/', views.photo_form, name="photo_form"),
    path('create_photo/', views.create_photo, name="create_photo"),
    path('create_post/', views.create_post, name="create_post"),
    path('photo/photo_detail/<int:post_id>/', views.photo_detail, name="photo_detail")
]