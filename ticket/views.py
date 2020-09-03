from django.shortcuts import render, redirect
from .models import Ticket
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from ticket import keys
import time
import json
import base64
import hashlib
import hmac
import requests

# Create your views here.
def form(request):
    return render(request, 'ticketForm.html')

def create(request):
    User = get_user_model()
    user = User.objects.get(username=request.user)

    Ticket(
        lesson_type=request.GET['lesson_type'],
        ticket_type=request.GET['ticket'],
        user_id=user.id,
        is_use = False,
        coupon = request.GET['ticket'].split('coupon')[1],
    ).save()

    send_sms(request.GET['ticket'].split('coupon')[1],user)

    return render(request, 'ticketSuccess.html')
    
def send_sms(coupon, user):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    signature = make_signature()

    message = user.first_name+"님이 이용권을 구매하셨습니다.\n이용권: "+ coupon + "회"

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
        new_ticket = Ticket.objects.get(id=id)
        try:
            today = datetime.today()
            #old ticket
            old_ticket = Ticket.objects.get(user_id=new_ticket.user_id, is_use=True, expired_date__gte=today, lesson_type=new_ticket.lesson_type)
            
            #update
            old_ticket.coupon += int(new_ticket.ticket_type.split('coupon')[1])
            if new_ticket.ticket_type.split('coupon')[1] == '10':
                old_ticket.expired_date += relativedelta(months=2)
            elif new_ticket.ticket_type.split('coupon')[1] == '20':
                old_ticket.expired_date += relativedelta(months=3)
            elif new_ticket.ticket_type.split('coupon')[1] == '30':
                old_ticket.expired_date += relativedelta(months=6)
            elif new_ticket.ticket_type.split('coupon')[1] == '50':
                old_ticket.expired_date += relativedelta(months=10)
            elif new_ticket.ticket_type.split('coupon')[1] == '100':
                old_ticket.expired_date += relativedelta(months=12)
            
            old_ticket.save()
            
            new_ticket.started_date = today - timedelta(1)
            new_ticket.expired_date = today - timedelta(1)
            new_ticket.save()


        except Ticket.DoesNotExist:
            #insert
            new_ticket.is_use = True
            new_ticket.started_date = datetime.now()

            if new_ticket.ticket_type.split('coupon')[1] == '10':
                new_ticket.expired_date = datetime.now() + relativedelta(months=2)
            elif new_ticket.ticket_type.split('coupon')[1] == '20':
                new_ticket.expired_date = datetime.now() + relativedelta(months=3)
            elif new_ticket.ticket_type.split('coupon')[1] == '30':
                new_ticket.expired_date = datetime.now() + relativedelta(months=6)
            elif new_ticket.ticket_type.split('coupon')[1] == '50':
                new_ticket.expired_date = datetime.now() + relativedelta(months=10)
            elif new_ticket.ticket_type.split('coupon')[1] == '100':
                new_ticket.expired_date = datetime.now() + relativedelta(months=12)

            new_ticket.save()
        
        tickets = Ticket.objects.filter(is_use=False, started_date=None, expired_date=None)
        context = {'tickets': tickets}
        return render(request, 'ticketList.html', context)
    else:
        return redirect('index')

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
        
        tickets = Ticket.objects.select_related('user').filter(is_use=False, started_date=None, expired_date=None).order_by('id')

        context = {
            'tickets': tickets
        }
        return render(request, 'ticketList.html', context)
    else:
        return redirect('index')