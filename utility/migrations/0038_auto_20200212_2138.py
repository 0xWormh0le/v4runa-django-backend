# Generated by Django 2.2 on 2020-02-13 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0037_monthlyreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyreport',
            name='name',
            field=models.CharField(blank=True, help_text='By default, file will be downloaded as a name of {Water utility name}-{year}-{month} form.<br/>Override if you want to customize it.', max_length=512, null=True),
        ),
    ]
