from django.shortcuts import render, redirect
import json
from django.views import View
from django.http  import JsonResponse,HttpResponse
# from .models      import Users
import bcrypt
import jwt
from acbaseball.settings import SECRET_KEY
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ticket.models import Ticket

# Create your views here.

def signup(request):
    return render(request, 'signup.html')

def create(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['username'],
            first_name = request.POST['first_name'],
            password=request.POST['password'],
            email=request.POST['email']
        )
        auth.login(request,user)
    return redirect('index')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'ID 혹은 PW가 잘못되었습니다.'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def list(request):
    user_model = get_user_model()    
    users = user_model.objects.all()
    context = {'users': users}
    return render(request, 'accountsList.html', context)    

def detail(request, id):
    user = User.objects.get(id=id)
    # ticket = Ticket.objects.get(id=)
    context = {'user': user}
    return render(request, 'accountsDetail.html')