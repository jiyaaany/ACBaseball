# Generated by Django 2.0.13 on 2020-12-05 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_ticketlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketlog',
            name='is_use',
            field=models.BooleanField(default=True),
        ),
    ]
