# Generated by Django 2.2 on 2019-12-24 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0023_auto_20191223_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nontcrsample',
            name='facility',
            field=models.ForeignKey(help_text='Facility', null=True, on_delete=django.db.models.deletion.CASCADE, to='utility.Facility'),
        ),
    ]
