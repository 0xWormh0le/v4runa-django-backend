import os
from django.utils.crypto import get_random_string
from datetime import datetime


def monthly_report_upload(instance, filename):
    name, ext = os.path.splitext(filename)
    filepath = '{}/{}/{}-{}'.format(
        'monthly-reports',
        instance.water_utility.id,
        instance.date.strftime('%Y-%m'),
        get_random_string(5)
    )

    return '{}{}'.format(filepath, ext) if ext else filepath


def pump_compare_upload(instance, filename):
    name, ext = os.path.splitext(instance.name)
    filepath = '{}/{}/{}-{}-{}'.format(
        'pump-compares',
        instance.user.id,
        datetime.now().strftime('%Y-%m-%d'),
        name,
        get_random_string(5)
    )

    return '{}{}'.format(filepath, ext) if ext else filepath
