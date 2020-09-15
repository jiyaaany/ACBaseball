from django.shortcuts import render
from cafe.models import Notice

# Create your views here.
def index(request):
    notices = Notice.objects.all().order_by('-id')[:3]
    return render(request, 'index.html', {'notices': notices})

def time(request):
    return render(request, 'time.html')

def fare(request):
    return render(request, 'fare.html')

def center(request):
    return render(request, 'center.html')
def way(request):
    return render(request, 'way.html')

def facility(request):
    return render(request, 'facility.html')