from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Schedule
from accounts.models import Users
import datetime

# Create your views here.
def list(request):
    schedules = Schedule.objects.all()
    context = {'schedules': schedules}
    return render(request, 'scheduleList.html', context)

def create(request):
    print('create')
    print(type(request.POST['schedule_name']))
    user_id = Users.objects.get(user_id='jiyaaany')

    print(user_id)
    try:
        Schedule(
            shedule_name = request.POST['schedule_name'],
            user_id = 'jiyaaany',
            schedule_date = datetime.datetime.strptime(request.POST['schedule_date']+':00', '%Y-%m-%d %H:%M:%S'),
            schedule_desc= request.POST['schedule_desc'] 
        ).save()
        return redirect('list')
    except Exception:
        return redirect('form')

def form(request):
    return render(request, 'scheduleForm.html')

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

class IndexView(View):
    def post(self, request):
        return JsonResponse