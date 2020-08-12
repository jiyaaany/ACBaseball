from django.db import models
from accounts.models import Users

# Create your models here.
class Ticket(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length = 50)
    is_use = models.BooleanField(default=False, blank=False)
    coupon = models.IntegerField(default=0, blank=False)
    started_date = models.DateTimeField()
    expired_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ticket"