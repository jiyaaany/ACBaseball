from django.db import models
from accounts.models import Users

# Create your models here.
class Ticket(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length = 50)

    class Meta:
        db_table = "ticket"