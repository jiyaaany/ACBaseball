from django.shortcuts import render, redirect
from ticket.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib import messages
import datetime
from datetime import datetime, timedelta
from lesson.models import Lesson_info, Lesson_user
from django.db.models import Count
from django.contrib.auth import get_user_model
from dateutil.relativedelta import relativedelta
import requests
from lesson import keys
import time
import json
import base64
import hashlib
import hmac

# Create your views here.
def form(request, type):
    if request.user.is_anonymous :
        messages.info(request, '로그인 후 이용해주세요.')
        return redirect('accounts:login')
    else:
        user_model = get_user_model()
        user = user_model.objects.get(username=request.user)
        if request.method == 'GET':
            try:
                Ticket.objects.get(user_id=user.id, lesson_type=type, is_use=1)

                return render(request, 'lessonForm.html', { 'type': type })
            except Ticket.DoesNotExist:
                messages.info(request, '사용 가능한 이용권이 없습니다. 먼저 이용권을 구매해주세요.')
                return render(request, 'ticketForm.html')
        
def list(request):
    today = datetime.today()
    lesson_user = Lesson_user.objects.select_related('lesson_info').select_related('user')
    lesson_user = lesson_user.order_by('-lesson_info.date', 'lesson_info.time')

    return render(request, 'lessonList.html', {'lesson_user': lesson_user, 'today': today})

def apply(request, id):
    lesson_info = Lesson_info.objects.get(id=id)
    user_model = get_user_model()
    user = user_model.objects.get(username=request.user)
    ticket = Ticket.objects.get(user_id=user.id, lesson_type=lesson_info.lesson_type, is_use=True)

    if lesson_info.use_num < lesson_info.user_num:
        lesson_info.use_num += 1
        lesson_info.save()
    
    Lesson_user(
        lesson_info_id=id,
        user_id=user.id
    ).save()

    # started_date, expired_date 처리

    ticket.coupon -= 1

    if ticket.coupon == 0:
        ticket.is_use = False

    ticket.save()

    #SMS 보내기
    send_sms(lesson_info, user, 'insert')

    param = {
        'lesson_info': lesson_info,
        'user': user,
        'ticket': ticket
    }
    return render(request, 'lessonSuccess.html', param)

def send_sms(lesson_info, user, type):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    signature = make_signature()

    if type == 'insert':
        message = user.first_name+"님 예약이 완료되었습니다.\n예약일자: "+str(lesson_info.date)+"\n예약시간: "+lesson_info.time
    elif type == 'delete':
        message = user.first_name+"님 예약이 취소되었습니다.\n예약일자: "+str(lesson_info.date)+"\n예약시간: "+lesson_info.time

    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': "D8n9QBfdjxFYrnRH1gAK",
        'x-ncp-apigw-signature-v2': signature
    }

    body = {
        "type":"SMS",
        "contentType":"COMM",
        "countryCode":"82",
        "from":"01035050076",
        "content":message,
        "messages":[
            {
                "to":str(user.email),
                "content":message
            },
            {
                "to":"01035050076",
                "content":message
            }
        ]
    }

    body = json.dumps(body)

    response = requests.post("https://sens.apigw.ntruss.com/sms/v2/services/"+keys.service_id+"/messages", headers=headers, data=body)
    response.raise_for_status()

def make_signature():
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_key = keys.access_key				# access key id (from portal or Sub Account)
    secret_key = keys.secret_key
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    uri = "/sms/v2/services/"+keys.service_id+"/messages"
    message = method + " " + uri + "\n" + timestamp + "\n"+ access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return signingKey

def photo(request):
    return render(request, 'photo.html')
def movie(request):
    return render(request, 'movie.html')

def delete(request, id):
    lesson_user = Lesson_user.objects.get(id=id)
    lesson_user.delete()

    user_model = get_user_model()
    user = user_model.objects.get(id=lesson_user.user_id)

    lesson_info = Lesson_info.objects.get(id=lesson_user.lesson_info_id)
    lesson_info.use_num -= 1
    lesson_info.save()

    try:
        live_ticket = Ticket.objects.get(user_id=user.id, lesson_type=lesson_info.lesson_type, is_use=True)
        live_ticket.coupon += 1
        live_ticket.save()

    except Ticket.DoesNotExist:
        last_ticket = Ticket.objects.get(user_id=user.id, lesson_type=lesson_info.lesson_type).order_by('-expired_date')[:1]
        Ticket(
            lesson_type=lesson_info.lesson_type,
            ticket_type='coupon10',
            create_date=datetime.now(),
            started_date=datetime.now(),
            expired_date=last_ticket.expired_date,
            user_id=user.id,
            is_use = True,
            coupon = 1,
        ).save()

    #SMS 보내기
    send_sms(lesson_info, user, 'delete')

    param_lesson_user = Lesson_user.objects.select_related('lesson_info').select_related('user')
    param_lesson_user = param_lesson_user.filter(user_id=user.id)
    param_lesson_user = param_lesson_user.order_by('-lesson_info.date', '-lesson_info.time')

    tickets = Ticket.objects.filter(user_id=user.id, is_use=True, coupon__gt=0, expired_date__gt=datetime.now(), started_date__lt=datetime.now())

    context = {
        'user': user,
        'tickets': tickets,
        'lessons': param_lesson_user
    }

    if request.user.is_superuser:
        admin_lesson_user = Lesson_user.objects.select_related('lesson_info').select_related('user')
        admin_lesson_user = admin_lesson_user.order_by('lesson_info.date', 'lesson_info.time')

        return render(request, 'lessonList.html', {'lesson_user': admin_lesson_user})
    else:
        return render(request, 'accountsDetail.html', context)

def get(request, date):
    aWeekDay = ['월', '화', '수', '목', '금', '토', '일']
    dtDate = datetime.strptime(date, '%Y-%m-%d')
    weekday = aWeekDay[dtDate.weekday()]
    lesson_day = dtDate.strftime('%m월 %d일') + '(' + weekday + ")"

    lesson_infos = Lesson_info.objects.filter(date=date, lesson_type=request.GET['type'])
    lesson_users = Lesson_user.objects.select_related('lesson_info').select_related('user')
    
    return render(request, 'lessonDetail.html', { 'lesson_day': lesson_day, 'lesson_infos': lesson_infos, 'lesson_users': lesson_users })