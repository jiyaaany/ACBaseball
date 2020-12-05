from django.shortcuts import render, redirect
from .models import Ticket, TicketLog
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.contrib import messages
from ticket import keys
import time
import json
import base64
import hashlib
import hmac
import requests

# Create your views here.
def form(request):
    if request.user.is_anonymous :
        messages.info(request, '로그인 후 이용해주세요.')
        return redirect('accounts:login')
    return render(request, 'ticketForm.html')

def create(request):
    User = get_user_model()
    user = User.objects.get(username=request.user)

    TicketLog(
        user_id = user.id,
        ticket_type = request.GET['ticket']
    ).save()

    strCoupon = ''

    for idx, lesson in enumerate(request.GET['ticket'].split(';')):
        if lesson:
            bTicketType = lesson[0] == 'P'
            strCoupon += ('개인레슨 ' if bTicketType else '그룹레슨 ') + lesson[1:] + '회'

            if idx != len(request.GET['ticket'].split(';'))-2:
                strCoupon += ', '
    
    send_sms(strCoupon, user)

    return render(request, 'ticketSuccess.html')
    
def send_sms(strCoupon, user):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    signature = make_signature()

    message = user.first_name+"님이 이용권을 구매하셨습니다.\n이용권: "+ strCoupon

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

def update(request, id):
    if request.user.is_superuser:
        # new ticket
        newTicket = TicketLog.objects.get(id=id)

        for idx, ticket in enumerate(newTicket.ticket_type.split(';')):
            if ticket: 
                # 같은 종류의 이용권이 있을 때
                try:
                    oldTicket = Ticket.objects.get(user_id=newTicket.user_id, is_use=True, lesson_type=ticket[0])

                    oldTicket.coupon += int(ticket[1:])

                    # expired_date 처리

                    oldTicket.save()
                # 같은 종류의 이용권이 없을 때 
                except Ticket.DoesNotExist:
                    Ticket(
                        ticket_type = newTicket.ticket_type,
                        is_use = True,                 
                        started_date = datetime.today(),
                        coupon = ticket[1:],
                        user_id = newTicket.user_id,
                        lesson_type = ticket[0]
                    ).save()


        newTicket.is_use = False
        newTicket.save()

        ticketLogs = TicketLog.objects.all()

        return render(request, 'ticketList.html', { 'ticketLogs': ticketLogs })

def delete(request, id):
    if request.user.is_superuser:    
        ticket = Ticket.objects.get(id=id)
        ticket.is_use = False
        ticket.started_date = datetime.now() - timedelta(1)
        ticket.expired_date = datetime.now() - timedelta(1)
        ticket.save()

        tickets = Ticket.objects.all()
        tickets = tickets.filter(is_use=False, started_date=None, expired_date=None)
        tickets = tickets.order_by('id')
        context = {'tickets': tickets}

        return render(request, 'ticketList.html', context)
    else:
        return redirect('index')

def list(request):
    if request.user.is_superuser:
        user_model = get_user_model()
        user = user_model.objects.all()
        
        ticketLogs = TicketLog.objects.filter(is_use=True).select_related('user').order_by('id')

        context = { 'ticketLogs': ticketLogs }

        return render(request, 'ticketList.html', context)
    else:
        return redirect('index')