# Generated by Django 2.2 on 2019-12-23 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0014_auto_20191223_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tcrsampleschedule',
            name='original_sample',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.TcrSample'),
        ),
    ]