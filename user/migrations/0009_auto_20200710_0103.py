# Generated by Django 2.2 on 2020-07-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_newsignup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribe_desc',
            field=models.TextField(blank=True, help_text='User left text when he signed up', max_length=1024),
        ),
    ]
