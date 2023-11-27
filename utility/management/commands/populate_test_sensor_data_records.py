from django.core.management.base import BaseCommand
from datetime import datetime, date, timedelta
from random import randrange, random, sample

from utility.models import (
    Sensor,
    SensorDataRecord,
)
from utility.constants import WATER_REGULATIONS


def populate_test_sensor_record_data(start_date, end_date):
    total_count = Sensor.objects.count()
    # Assume 4 sensors have issues
    abnormal_sensor_count = 4
    abnormal_sensor_indices = sample(range(0, total_count), abnormal_sensor_count)
    issue_offset = (WATER_REGULATIONS['orp']['upper'] - WATER_REGULATIONS['orp']['lower']) * 0.2

    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    for idx, sensor in enumerate(Sensor.objects.all()):
        sensor.records.filter(
            recorded_at__gte=start_dt,
            recorded_at__lte=end_dt
        ).delete()
        dt = start_dt
        delta = timedelta(0)

        issue_start_delta = (end_dt - start_dt) * random()

        issue_type = 'lower' if random() > 0.5 else 'upper'
        while dt < end_dt:
            if idx in abnormal_sensor_indices and issue_start_delta < delta:
                offset = randrange(2, issue_offset)
                if issue_type == 'lower':
                    value = randrange(WATER_REGULATIONS['orp'][issue_type] - offset, WATER_REGULATIONS['orp'][issue_type] - 1)
                else:
                    value = randrange(WATER_REGULATIONS['orp'][issue_type] + 1, WATER_REGULATIONS['orp'][issue_type] + offset)
            else:
                value = randrange(WATER_REGULATIONS['orp']['lower'], WATER_REGULATIONS['orp']['upper'])

            record = SensorDataRecord(
                sensor=sensor,
                value_type='orp',
                recorded_at=dt,
                value=value
            )
            record.save()
            delta += timedelta(minutes=10)
            dt = start_dt + delta


def parse_date(dt):
    return datetime.strptime(dt, '%Y%m%d').date()


class Command(BaseCommand):
    help = ('Populates random walk test sensor data records')

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=parse_date, help='Inclusive start date to load the data for (YYYYMMDD)')
        parser.add_argument('end_date', type=parse_date, help='Inclusive end date to load the data for (YYYYMMDD)')

    def handle(self, *args, **options):
        start_date = options.get('start_date') or date.today()
        end_date = options.get('end_date') or date.today()
        populate_test_sensor_record_data(start_date, end_date)
