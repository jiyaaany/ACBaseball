from django.db import models
from django.conf import settings

# Create your models here.
class Lesson_info(models.Model):
    lesson_type = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=200)
    user_num = models.IntegerField()
    use_num = models.IntegerField(default=0)

    class Meta:
        db_table = "lesson_info"

class Lesson_user(models.Model):
    lesson_info = models.ForeignKey(Lesson_info, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "lesson_user"
