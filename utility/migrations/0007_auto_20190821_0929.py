# Generated by Django 2.2 on 2019-08-21 14:29

from django.db import migrations, models
import django.db.models.deletion


def populate_sensor_field(apps, schema_editor):
    Alert = apps.get_model('utility', 'Alert')
    for alert in Alert.objects.all():
        alert.sensor = alert.sensor_data_record.sensor
        alert.save()


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0006_alert_sensor_sensordatarecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(help_text='Sensor', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='utility.Sensor'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='sensor_data_record',
            field=models.OneToOneField(help_text='Sensor Data Record (should be the record of the same sensor specified in the `sensor` field)', on_delete=django.db.models.deletion.CASCADE, related_name='alert', to='utility.SensorDataRecord'),
        ),
        migrations.RunPython(populate_sensor_field),
        migrations.AlterField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(help_text='Sensor', on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='utility.Sensor'),
        ),
    ]
