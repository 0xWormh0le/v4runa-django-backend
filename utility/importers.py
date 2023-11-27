import csv
from io import StringIO
from django.utils.dateparse import parse_datetime

from common.utils import get_choice_id_by_label
from .models import (
    AssetFinance,
    WaterQuality,
    WaterUtility,
    Sensor,
    Technician,
)
from geo.models import Address
from user.models import User
from user.constants import ROLE_TECHNICIAN
from . import constants as cs


water_utilities_cache = {}


def _get_water_utility(water_system_id):
    if not water_system_id:
        return None
    water_utility = water_utilities_cache.get(water_system_id)
    if water_utility is None:
        water_utility = WaterUtility.objects \
            .filter(water_system_id=water_system_id) \
            .first()
        water_utilities_cache[water_system_id] = water_utility or False
    return water_utilities_cache[water_system_id]


def import_water_utilities(csv_file):
    file_data = StringIO(csv_file.read().decode("utf-8"))
    csv_reader = csv.DictReader(file_data)
    failed_rows = []
    for row in csv_reader:
        try:
            water_utility = WaterUtility.objects \
                .filter(water_system_id=row.get('water_system_id')) \
                .first()
            if water_utility is None:
                water_utility = WaterUtility(
                    water_system_id=row.get('water_system_id')
                )

            location = Address.objects.create(
                city=row.get('city'),
                state=row.get('state'),
                country=row.get('state') or 'US',
                latitude=row.get('latitude'),
                longitude=row.get('longitude'),
            )
            water_utility.location=location
            water_utility.name=row.get('name')
            water_utility.url=row.get('url')
            water_utility.population=row.get('population')
            water_utility.num_meters=row.get('num_meters')
            water_utility.primary_water_source_type=get_choice_id_by_label(row.get('primary_water_source_type'), cs.WATER_SOURCE_TYPE_CHOICES)
            water_utility.is_pws_activity_active=True if str(row.get('is_pws_activity_active')).lower == 'active' else False
            water_utility.water_system_type=get_choice_id_by_label(row.get('water_system_type'), cs.WATER_SYSTEM_TYPE_CHOICES)
            water_utility.save()
        except:
            failed_rows.append(row.get('water_system_id'))

    return failed_rows if len(failed_rows) > 0 else None


def import_asset_finance_data(csv_file):
    file_data = StringIO(csv_file.read().decode("utf-8"))
    csv_reader = csv.DictReader(file_data)
    failed_rows = []
    for row in csv_reader:
        water_system_id = row.get('water_system_id')
        water_utility = _get_water_utility(water_system_id)
        year = row.get('year')
        asset_name = row.get('asset_name')

        if water_utility:
            water_quality = AssetFinance.objects \
                .filter(year=year, water_utility=water_utility, asset_name=asset_name) \
                .first()
            if water_quality is None:
                asset_finance = AssetFinance(
                    year=year, water_utility=water_utility, asset_name=asset_name
                )

            asset_finance.projected_unscheduled_amount = row.get('projected_unscheduled_amount') or None
            asset_finance.projected_scheduled_amount = row.get('projected_scheduled_amount') or None
            asset_finance.allocated_budget = row.get('allocated_budget') or None
            asset_finance.average_service_life = row.get('average_service_life') or None
            asset_finance.save()
        else:
            failed_rows.append(row.get('water_system_id'))

    return failed_rows if len(failed_rows) > 0 else None


def import_water_quality_history(csv_file):
    file_data = StringIO(csv_file.read().decode("utf-8"))
    csv_reader = csv.DictReader(file_data)
    failed_rows = []
    for row in csv_reader:
        water_system_id = row.get('water_system_id')
        water_utility = _get_water_utility(water_system_id)

        if water_utility:
            dt = parse_datetime(row.get('date'))
            water_quality = WaterQuality.objects \
                .filter(date=dt, water_utility=water_utility) \
                .first()
            if water_quality is None:
                water_quality = WaterQuality(
                    date=dt, water_utility=water_utility
                )
            water_quality.barium = row.get('barium')
            water_quality.fluoride = row.get('fluoride')
            water_quality.nitrate = row.get('nitrate')
            water_quality.sodium = row.get('sodium')
            water_quality.haa5 = row.get('haa5')
            water_quality.tthm = row.get('tthm')
            water_quality.copper = row.get('copper')
            water_quality.lead = row.get('lead')
            water_quality.orp = row.get('orp')
            water_quality.chlorine = row.get('chlorine')
            water_quality.save()
        else:
            failed_rows.append(row.get('water_system_id'))

    return failed_rows if len(failed_rows) > 0 else None


def import_sensors(csv_file):
    file_data = StringIO(csv_file.read().decode("utf-8"))
    csv_reader = csv.DictReader(file_data)
    failed_rows = []
    for row in csv_reader:
        device_id = row.get('device_id')
        water_system_id = row.get('water_system_id')
        water_utility = _get_water_utility(water_system_id)
        print(water_system_id, water_utility)
        if water_utility:
            try:
                sensor = Sensor.objects.filter(device_id=device_id).first()
                if sensor is None:
                    sensor = Sensor(device_id=device_id)
                sensor.water_utility = water_utility
                sensor.latitude = float(row.get('latitude'))
                sensor.longitude = float(row.get('longitude'))
                sensor.save()
            except:
                failed_rows.append(device_id)
        else:
            failed_rows.append(device_id)

    return failed_rows if len(failed_rows) > 0 else None


def import_technicians(csv_file):
    file_data = StringIO(csv_file.read().decode("utf-8"))
    csv_reader = csv.DictReader(file_data)
    failed_rows = []
    for row in csv_reader:
        email = row.get('email')
        first_name = row.get('first_name')
        last_name = row.get('last_name')
        user = User.objects.filter(email=email).first()
        technician = None
        if user:
            if hasattr(user, 'technician'):
                technician = user.technician
            elif user.role == ROLE_TECHNICIAN:
                technician = Technician(user=user)
            else:
                failed_rows.append(email)
                continue
        else:
            user = User.objects.create(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                role=ROLE_TECHNICIAN,
            )
            password = User.objects.make_random_password()
            user.set_password(password)
            technician = Technician(user=user)
        
        technician.hourly_rate = float(row.get('hourly_rate'))
        technician.preferred_job_type = row.get('preferred_job_type')
        technician.save()

    return failed_rows if len(failed_rows) > 0 else None
