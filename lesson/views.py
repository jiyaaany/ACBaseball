from django.shortcuts import render
from ticket.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib import messages
import datetime
from lesson.models import Lesson_info, Lesson_user
from django.db.models import Count
from django.contrib.auth import get_user_model

# Create your views here.
def form(request):
    user_model = get_user_model()
    user = user_model.objects.get(username=request.user)
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(user_id=user.id, lesson_type=request.POST['lesson_type'])
            param = {'lesson_type':request.POST['lesson_type'], 'date':request.POST['date'], 'time':request.POST['time']}
            lesson_info = Lesson_info.objects.filter(lesson_type=request.POST['lesson_type'], date=request.POST['date'].replace(".","-"), time=request.POST['time'])
            context = {
                'param': param,
                'lesson_info':lesson_info
            }
            return render(request, 'lessonForm.html', context)    
        except Ticket.DoesNotExist:
            messages.info(request, '사용 가능한 이용권이 없습니다. 먼저 이용권을 구매해주세요.')
            return render(request, 'ticketForm.html')        
    else:
        try:
            ticket = Ticket.objects.get(user_id=user.id)
            return render(request, 'lessonForm.html')
        except Ticket.DoesNotExist:
            messages.info(request, '사용 가능한 이용권이 없습니다. 먼저 이용권을 구매해주세요.')
            return render(request, 'ticketForm.html')

def list(request):
    print('list')
    # today = datetime.datetime.date(datetime.datetime.today())
    # lesson_info = Lesson_info.objects.filter(date__gte=today).values('date').annotate(Count('id')).order_by('date')
    lesson_info = Lesson_info.objects.all()    
    return render(request, 'lessonList.html', {'lesson_info': lesson_info})

def apply(request, id):
    lesson_info = Lesson_info.objects.get(id=id)
    user_model = get_user_model()
    user = user_model.objects.get(username=request.user)
    ticket = Ticket.objects.get(user_id=user.id)
    
    Lesson_user(
        lesson_info_id=id,
        user_id=user.id
    ).save()

    if lesson_info.use_num < lesson_info.user_num:
        lesson_info.use_num += 1
        lesson_info.save()
    else:
        messages.info(request, '해당 시간의 레슨은 신청할 수 없습니다. (정원초과)')
        return render(request, 'lessonSuccess.html')        
    
    if ticket.coupon > 0:     
        ticket.coupon -= 1
        ticket.save()
    else:
        messages.info(request, '이용권을 모두 사용하셨습니다.')
        return render(request, 'ticketForm.html')
    
    param = {
        'lesson_info': lesson_info,
        'user': user,
        'ticket': ticket
    }
    return render(request, 'lessonSuccess.html', param)