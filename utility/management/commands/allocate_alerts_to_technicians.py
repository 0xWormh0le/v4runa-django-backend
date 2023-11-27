from django.core.management.base import BaseCommand
from datetime import datetime, date, timedelta
from math import floor
from random import random, sample

from utility.models import (
    Alert,
    ResourceAllocation,
    ResourceAllocationCalendar,
    Technician,
)
from utility import constants as cs


def get_random_closing_date():
    closing_dt_delta = 30 * random() # get a random day number in one month
    return date.today() + timedelta(days=closing_dt_delta)


def get_random_department():
    idx = floor(len(cs.DEPARTMENT_CHOICES) * random())
    return cs.DEPARTMENT_CHOICES[idx][0]


def get_random_job_type():
    idx = floor(len(cs.JOB_TYPE_CHOICES) * random())
    return cs.JOB_TYPE_CHOICES[idx][0]


def resolve_expired_allocations():
    resource_allocations = ResourceAllocation.objects.filter(closing_date__lte=date.today())
    Technician.objects.filter(current_job__in=resource_allocations).update(current_job=None)


def get_location_from_alert(alert):
    location = alert.sensor.water_utility.location
    location.pk = None
    location.save()
    return location


def allocate_alerts_to_technicians():
    resolve_expired_allocations()

    alerts = Alert.objects.filter(status=cs.ALERT_STATUS_IN_PROCESS).order_by('-reported_at')
    technicians = Technician.objects.filter(current_job__isnull=True)
    count = min(alerts.count(), technicians.count())
    alerts = list(alerts)
    technicians = list(technicians)
    for idx in range(0, count):
        print(count, idx)
        alert = alerts[idx]
        technician = technicians[idx]

        resource_allocation = ResourceAllocation.objects.create(
            alert=alert,
            assignee=technician,
            job_number=ResourceAllocation.objects.get_new_job_number(),
            closing_date=get_random_closing_date(),
            start_date=date.today(),
            department=get_random_department(),
            job_type=get_random_job_type(),
            location=get_location_from_alert(alert),
            salary=technician.hourly_rate,
        )
        technician.current_job = resource_allocation
        technician.save()
        alert.status = cs.ALERT_STATUS_ONGOING
        alert.save()

        days = (resource_allocation.closing_date - date.today()).days
        selected_days = sample(range(0, days), int(days * 0.8))
        allocation_dates = []
        for days in selected_days:
            jc = ResourceAllocationCalendar(
                allocation=resource_allocation,
                date=date.today() + timedelta(days=days),
            )
            allocation_dates.append(jc)
        ResourceAllocationCalendar.objects.bulk_create(allocation_dates)


class Command(BaseCommand):
    help = ('Allocate new alerts to technicians')

    def handle(self, *args, **options):
        allocate_alerts_to_technicians()
