from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def time(request):
    return render(request, 'time.html')

def fare(request):
    return render(request, 'fare.html')