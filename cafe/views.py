from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def create(request):
    Notice(
        title=request.POST['content'][0:250],
        content=request.POST['content'],
    ).save()

    notices = Notice.objects.all().order_by('-id')

    return render(request, 'cafeList.html', {'notices': notices})
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

def list(request):
    notices = Notice.objects.all().order_by('-id')

    return render(request, 'cafeList.html', {'notices': notices})