from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from utility.models import Sensor
from user.models import User, Profile
from api.reports.helpers import weekly_report_data


def send_weekly_report_mail():
    sensors = Sensor.objects.filter(water_utility__profile__is_approved=True, water_utility__profile__user__is_active=True).all()
    for sensor in sensors:
        profiles = sensor.water_utility.profile_set.all()
        receivers = map(lambda profile: profile.user.email, profiles)
        send_mail(
            _('Varuna Weekly Report'),
            None,
            settings.DEFAULT_FROM_EMAIL,
            list(receivers),
            html_message=render_to_string('emails/weekly_report.html', weekly_report_data(sensor.pk, 'chlorine')),
            fail_silently=True
        )
    

class Command(BaseCommand):
    help = ('Send weekly report email')

    def handle(self, *args, **options):
        send_weekly_report_mail()
