# Generated by Django 2.2 on 2020-02-18 18:48

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20200217_2110'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
