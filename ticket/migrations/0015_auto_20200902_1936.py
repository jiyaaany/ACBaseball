# Generated by Django 2.0.13 on 2020-09-02 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0014_auto_20200817_2014'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='ticket',
        #     name='lesson_type',
        #     field=models.CharField(max_length=128, null=True),
        # ),
        # migrations.AddField(
        #     model_name='ticket',
        #     name='user',
        #     field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        # ),
    ]
