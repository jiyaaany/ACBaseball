from django.shortcuts import render, redirect
from .models import Ticket
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model

# Create your views here.
def form(request):
    return render(request, 'ticketForm.html')

def create(request):
    User = get_user_model()
    user = User.objects.get(username=request.user)
    Ticket(
        lesson_type=request.GET['lesson_type'],
        ticket_type=request.GET['ticket'],
        user_id=user.id
    ).save()
    return render(request, 'ticketsuccess.html')

def update(request, id):
    if request.user.is_superuser:
        ticket = Ticket.objects.get(id=id)
        ticket.is_use = True
        # ticket.started_date = datetime.now()
        ticket.coupon = int(ticket.ticket_type.split('coupon')[1])
        # if ticket.ticket_type.find('month') > -1:
            # ticket.expired_date = datetime.now() + relativedelta(months=ticket.ticket_type.split('month')[1])
        # elif ticket.ticket_type.find('coupon') > -1:
            # ticket.coupon = int(ticket.ticket_type.split('coupon')[1])
            # ticket.expired_date = datetime.now() + relativedelta(months=2)

        ticket.save()
        
        tickets = Ticket.objects.all()
        tickets = tickets.filter(is_use=False, started_date=None, expired_date=None)
        tickets = tickets.order_by('id')
        context = {'tickets': tickets}
        return render(request, 'ticketList.html', context)
    else:
        return redirect('index')

def delete(request, id):
    if request.user.is_superuser:    
        ticket = Ticket.objects.get(id=id)
        ticket.is_use = False
        ticket.started_date = datetime.now()
        ticket.expired_date = datetime.now()
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