# Generated by Django 2.2 on 2020-01-17 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0032_auto_20200108_2305'),
        ('user', '0002_auto_20190929_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='water_utility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.WaterUtility'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'General Manager'), (3, 'Operation Manager'), (4, 'Customer'), (5, 'Technician')], default=1),
        ),
    ]
