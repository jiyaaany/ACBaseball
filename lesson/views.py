from django.shortcuts import render
from ticket.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib import messages
import datetime
from lesson.models import Lesson_info, Lesson_user
from django.db.models import Count

# Create your views here.
def form(request):
    t = ['월', '화', '수', '목', '금', '토', '일']
    today = datetime.datetime.date(datetime.datetime.today())
    Users = get_user_model()
    user = Users.objects.get(username=request.user)
    try:
        ticket = Ticket.objects.get(user_id=user.id)
        context = {'today': today, 't':t[today.weekday()],'ticket': ticket}
        return render(request, 'lessonForm.html', context)
    except Ticket.DoesNotExist:
        messages.info(request, '사용 가능한 이용권이 없습니다. 먼저 이용권을 구매해주세요.')
        return render(request, 'ticketForm.html')

def list(request):
    print('list')
    # today = datetime.datetime.date(datetime.datetime.today())
    # lesson_info = Lesson_info.objects.filter(date__gte=today).values('date').annotate(Count('id')).order_by('date')
    lesson_info = Lesson_info.objects.all()    
    return render(request, 'lessonList.html', {'lesson_info': lesson_info})

# def list(request, date):
#     return render(request, 'lessonList.html')"