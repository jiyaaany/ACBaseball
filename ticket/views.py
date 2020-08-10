from django.shortcuts import render
from .models import Ticket
from accounts.models import Users

# Create your views here.
def form(request):
    return render(request, 'ticketForm.html')

def create(request):
    print(request.user.user_id)
    user = Users.objects.get(user_id="jiyaaany")
    print(user)
    Ticket(
        ticket_type=request.GET['ticket'],
        user=user
    ).save()
    return render(request, 'ticketsuccess.html')