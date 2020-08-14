from django.shortcuts import render
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
        ticket_lesson=request.GET['ticket_lesson'],
        ticket_type=request.GET['ticket'],
        user_id=user.id
    ).save()
    return render(request, 'ticketsuccess.html')

def update(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.is_use = True
    ticket.started_date = datetime.now()
    
    if ticket.ticket_type.find('month') > -1:
        ticket.expired_date = datetime.now() + relativedelta(months=ticket.ticket_type.split('month')[1])
    elif ticket.ticket_type.find('coupon') > -1:
        ticket.coupon = int(ticket.ticket_type.split('coupon')[1])
        ticket.expired_date = datetime.now() + relativedelta(months=2)

    ticket.save()

    tickets = Ticket.objects.all()
    tickets = tickets.filter(is_use=False, started_date=None, expired_date=None)
    tickets = tickets.order_by('id')
    context = {'tickets': tickets}
    return render(request, 'ticketList.html', context)

def delete(request, id):
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

def list(request):
    # tickets = Ticket.objects.all()
    # tickets = tickets.filter(is_use=False, started_date=None, expired_date=None)
    # tickets = tickets.order_by('id')
    User = get_user_model()
    # print(Ticket.objects.prefetch_related('auth_user__id'))
    tickets = Ticket.objects.filter(is_use=False, started_date=None, expired_date=None).order_by('id')
    # .select_related(User)

    print(tickets)
    context = {
        'tickets': tickets
    }
    return render(request, 'ticketList.html', context)