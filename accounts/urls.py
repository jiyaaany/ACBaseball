from django.urls import path
from . import views
from .views import View
# from .views import CreateView, LoginView

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('findIDForm/', views.findIDForm, name='findIDForm'),
    path('findID/', views.findID, name='findID'),
    path('findPWForm/', views.findPWForm, name='findPWForm'),
    path('findPW/', views.findPW, name='findPW'),
    path('search/', views.search, name='search')
]