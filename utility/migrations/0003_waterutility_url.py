# Generated by Django 2.2 on 2019-08-08 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0002_waterquality'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterutility',
            name='url',
            field=models.URLField(blank=True, help_text='Water Utility Resource URL', null=True),
        ),
    ]
