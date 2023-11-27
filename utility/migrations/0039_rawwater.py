# Generated by Django 2.2 on 2020-04-08 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0038_auto_20200212_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawWater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_inf_flow_gpm', models.FloatField(help_text='Flow coming into the Waterplant (generated from the pumps running)')),
                ('p2_speed_fbk_scaled', models.FloatField(help_text='Speed of Pump 2 in Hz')),
                ('p3_speed_fbk_scaled', models.FloatField(help_text='Speed of Pump 3 in Hz')),
                ('p1_start_stop', models.IntegerField(help_text='Pump 1 Run Command (not a variable speed pump)')),
                ('p2_start_stop', models.IntegerField(help_text='Pump 2 Run Command')),
                ('p3_start_stop', models.IntegerField(help_text='Pump 3 Run Command')),
                ('inf_flow_setpoint_control', models.IntegerField(help_text='System running in Auto')),
                ('orp_scaled', models.FloatField()),
                ('ph_scaled', models.FloatField()),
                ('p2_speed_cmd_real', models.FloatField(help_text='Pump 2 Speed Command')),
                ('p3_speed_cmd_real', models.FloatField(help_text='Pump 3 Speed Command')),
                ('inf_flow_total_today', models.FloatField(help_text='Flow total in Gallons')),
                ('inf_flow_total_yesterday', models.FloatField(help_text='Flow total in Gallons')),
                ('inf_flow_total_mg', models.FloatField(help_text='Flow total in Million of Gallons')),
                ('inf_flow_setpoint', models.FloatField(help_text='Flow setpoint that is trying to be maintained')),
            ],
        ),
    ]
