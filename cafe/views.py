from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def create(request):
    return render(request, 'index.html')
    # profile.photo = request.FILES['photo']

def form(request):
    return render(request, 'index.html')

def detail(request):
    return render(request, 'index.html')

def photo(request):
    return render(request, 'index.html')

def movie(request):
    return render(request, 'index.html')

def create_photo(request):
    return render(request, 'index.html')

def create_post(request):
    return render(request, 'index.html')

def photo_form(request):
    return render(request, 'index.html')

def photo_detail(request, post_id):
    return render(request, 'index.html')