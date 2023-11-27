from . import constants as cs
from django.dispatch import receiver
from django_cleanup.signals import (
    cleanup_pre_delete,
    cleanup_post_delete
)


__all__ = [
    'get_alert_type',
    'check_and_create_alert',
]


# @receiver(cleanup_pre_delete)
def save_parent_path(**kwargs):
    kwargs['file'].name_backup = kwargs['file'].name


# @receiver(cleanup_post_delete)
def delete_parent_if_empty(**kwargs):
    storage = kwargs['file'].storage
    name = kwargs['file'].name_backup
    parent_path = name[:name.rfind('/')]
    directories, files = storage.listdir(parent_path)
    if len(directories) + len(files) == 0:
        storage.delete(parent_path)


def get_alert_type(record):
    if record.value_type == cs.CONTAMINATION_CHLORINE:
        if record.value <= 0.2:
            return (cs.ALERT_TYPE_WARNING, 0.2, False)
        elif record.value >= 2:
            return (cs.ALERT_TYPE_SERIOUS, 2, True)

    elif record.value_type == cs.CONTAMINATION_ORP:
        if record.value < 200:
            return (cs.ALERT_TYPE_CRITICAL, 200, False)
        elif record.value > 600:
            return (cs.ALERT_TYPE_WARNING, 600, True)

    elif record.value_type == cs.SENSOR_VALUE_TURBIDITY:
        if record.value >= 10:
            return (cs.ALERT_TYPE_CRITICAL, 10, True)
        elif record.value >= 2:
            return (cs.ALERT_TYPE_SERIOUS, 2, True)
        elif record.value >= 0.5:
            return (cs.ALERT_TYPE_WARNING, 0.5, True)

    elif record.value_type == cs.SENSOR_VALUE_PH:
        if record.value > 8.5:
            return (cs.ALERT_TYPE_WARNING, 8.5, True)
        elif record.value < 6.5:
            return (cs.ALERT_TYPE_WARNING, 6.5, False)
    
    elif record.value_type == cs.SENSOR_VALUE_WATER_TEMPERATURE:
        farenheit = record.value * 9 / 5 + 32
        if farenheit > 72:
            return (cs.ALERT_TYPE_WARNING, 72, True)
        elif farenheit < 50:
            return (cs.ALERT_TYPE_WARNING, 50, False)

    elif record.value_type == cs.SENSOR_VALUE_CONDUCTIVITY:
        if record.value > 800:
            return (cs.ALERT_TYPE_WARNING, 800, True)
        elif record.value < 200:
            return (cs.ALERT_TYPE_WARNING, 200, False)

    return (cs.ALERT_TYPE_NONE, 0, True)

def chemical_name(chemical):
    for ch in cs.SENSOR_VALUE_CHOICES:
        if ch[0] == chemical:
            return ch[1] 
    return None

def check_and_create_alert(record):
    from .models import Alert

    alert = Alert.objects.filter(
        sensor_data_record__sensor=record.sensor,
        sensor_data_record__value_type=record.value_type,
        reported_at__lte=record.recorded_at,
    ).order_by('-reported_at').first()
    
    (alert_type, threshhold, direction) = get_alert_type(record)
    message = '{} of #{} has reported {} {} {}'.format(
        chemical_name(record.value_type),
        record.sensor.format_with_location,
        'above' if direction else 'below',
        threshhold,
        '°F' if record.value_type == cs.SENSOR_VALUE_WATER_TEMPERATURE else record.unit
    )

    if alert and alert.status != cs.ALERT_STATUS_RESOLVED:
        if alert_type == cs.ALERT_TYPE_NONE:
            alert.status = cs.ALERT_STATUS_RESOLVED
            alert.save()
        elif alert.status == cs.ALERT_STATUS_IN_PROCESS:
            modify_alert(alert, record, message, cs.ALERT_STATUS_IN_PROCESS)
        elif alert.status == cs.ALERT_STATUS_ONGOING:
            if alert.alert_type == alert_type:
                return
            elif alert.alert_type > alert_type:
                modify_alert(alert, record, message, cs.ALERT_STATUS_RESOLVED)
            create_alert(record, message, cs.ALERT_STATUS_IN_PROCESS)
    elif alert_type != cs.ALERT_TYPE_NONE:
        create_alert(record, message, cs.ALERT_STATUS_IN_PROCESS)


def modify_alert(alert, record, message, status):
    alert.alert_type = record.alert_type
    alert.message = message
    alert.sensor_data_record = record
    alert.sensor = record.sensor
    alert.reported_at = record.recorded_at
    alert.status = status
    alert.save()


def create_alert(record, message, status):
    from .models import Alert

    Alert.objects.create(
        alert_type=record.alert_type,
        message=message,
        sensor_data_record=record,
        sensor=record.sensor,
        reported_at=record.recorded_at,
        status=status
    )
