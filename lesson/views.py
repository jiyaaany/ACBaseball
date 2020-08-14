from django.shortcuts import render
from ticket.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.
def form(request):
    Users = get_user_model()
    user = Users.objects.get(username=request.user)
    try:
        ticket = Ticket.objects.get(user_id=3)
        return render(request, 'lessonForm.html', {'ticket': ticket})
    except Ticket.DoesNotExist:
        messages.info(request, '사용 가능한 이용권이 없습니다. 먼저 이용권을 구매해주세요.')
        return render(request, 'ticketForm.html')

