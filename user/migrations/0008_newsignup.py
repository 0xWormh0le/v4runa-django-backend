# Generated by Django 2.2 on 2020-02-21 03:25

from django.db import migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200219_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewSignup',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.user',),
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
    ]