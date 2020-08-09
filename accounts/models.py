from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
