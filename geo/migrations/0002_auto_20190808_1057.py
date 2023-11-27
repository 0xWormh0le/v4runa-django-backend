# Generated by Django 2.2 on 2019-08-08 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, help_text='ZIP5', max_length=32, null=True),
        ),
    ]
