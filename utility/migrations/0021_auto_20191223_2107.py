# Generated by Django 2.2 on 2019-12-24 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0020_auto_20191223_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tcrsample',
            name='lab_id',
            field=models.CharField(max_length=20),
        ),
    ]