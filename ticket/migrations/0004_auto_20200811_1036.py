# Generated by Django 2.0.13 on 2020-08-11 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20200811_1022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='create_date',
            new_name='created_date',
        ),
    ]
