from django.shortcuts import render, redirect

# Create your views here.
def book_schedule(request):
    return render(request, 'index.html')

def show_schedule(request):
    return render(request, 'index.html')

def schedule_form(request):
    return render(request, 'index.html')

def create_schedule(request):
    return render(request, 'index.html')

def schedule_detail(request, pk):
    return render(request, 'index.html')

def cancel_schedule(request, pk):
    return render(request, 'index.html')