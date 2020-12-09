from django.shortcuts import render
from cafe.models import Notice

# Create your views here.
def index(request):
    notice = Notice.objects.order_by('-id')[:1].get()
    print(notice)
    return render(request, 'index.html', {'notice': notice})

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

def kids_time(request):
    return render(request, 'kidsTime.html')

def kids_fare(request):
    return render(request, 'kidsFare.html')

def elite_time(request):
    return render(request, 'eliteTime.html')

def elite_fare(request):
    return render(request, 'eliteFare.html')