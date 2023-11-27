from django.db.models import (Avg, Min, Max)
from datetime import datetime, timedelta
from utility.models import Sensor, SensorDataRecord
from utility import constants as cs


def weekly_report_data(sensor_id, chemical):
    sensor = Sensor.objects.get(pk=sensor_id)
    today = datetime.now()

    week_start = today + timedelta(-today.weekday(), weeks=-1)
    week_end = today + timedelta(-today.weekday() - 1)

    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_end.replace(hour=23, minute=59, second=59, microsecond=999999)

    latest_data = SensorDataRecord.objects.filter(
        sensor_id=sensor_id,
        value_type=chemical).latest('recorded_at')
    below_05_count = SensorDataRecord.objects.filter(
        sensor_id=sensor_id,
        value_type=chemical,
        value__lt=0.5,
        recorded_at__gt=week_start,
        recorded_at__lt=week_end).count()
    above_25_count = SensorDataRecord.objects.filter(
        sensor_id=sensor_id,
        value_type=chemical,
        value__gt=2.5,
        recorded_at__gt=week_start,
        recorded_at__lt=week_end).count()
    avg = SensorDataRecord.objects.filter(
        sensor_id=sensor_id,
        value_type=chemical,
        recorded_at__gt=week_start,
        recorded_at__lt=week_end).aggregate(Avg('value'))['value__avg']
    min = SensorDataRecord.objects.filter(
        sensor_id=sensor_id,
        value_type=chemical,
        recorded_at__gt=week_start,
        recorded_at__lt=week_end).aggregate(Min('value'))['value__min']
    max = SensorDataRecord.objects.filter(
        sensor_id=sensor_id,
        value_type=chemical,
        recorded_at__gt=week_start,
        recorded_at__lt=week_end).aggregate(Max('value'))['value__max']
    
    return {
        'date': today.strftime('%Y-%m-%d'),
        'week_start': week_start.strftime('%Y-%m-%d'),
        'week_end': week_end.strftime('%Y-%m-%d'),
        'sensor_address': str(sensor.location),
        'latest_data': round(latest_data.value, 4) if latest_data else None,
        'below_05_count': below_05_count,
        'above_25_count': above_25_count,
        'avg': 0 if avg == None else round(avg, 4),
        'min': 0 if min == None else round(min, 4),
        'max': 0 if max == None else round(max, 4)
    }
