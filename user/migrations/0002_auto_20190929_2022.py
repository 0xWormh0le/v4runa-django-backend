# Generated by Django 2.2 on 2019-09-30 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'General Manager'), (3, 'Operation Manager'), (4, 'Consumer'), (5, 'Technician')], default=1),
        ),
    ]
