# Generated by Django 2.2 on 2020-04-14 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0039_rawwater'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawwater',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, help_text='Timestamp'),
        ),
    ]
