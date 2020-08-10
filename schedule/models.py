from django.db import models
from accounts.models import Users

# Create your models here.

class Schedule(models.Model):
    schedule_name = models.CharField(max_length=128, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    schedule_date = models.DateTimeField(blank=False)
    schedule_desc = models.CharField(max_length=256)

    class Meta:
        db_table = "schedule"