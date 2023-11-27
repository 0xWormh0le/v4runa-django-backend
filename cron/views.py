from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.management import call_command

# Create your views here.

class WeeklyReportMailView(APIView):
    """
    Send weekly report mail.
    """

    def get(self, request):
        cron_header = 'X-Appengine-Cron'
        if not cron_header in request.headers:
            raise ValidationError('This is not a cron request from App Engine')
        if request.headers.get(cron_header) != 'true':
            raise ValidationError('This is not a cron request from App Engine')
        call_command('weekly_report_mail')
        return Response()


class AfterDeployView(APIView):
    """
    Send weekly report mail.
    """

    def get(self, request):
        job_header = 'X-Appengine-AfterDeploy'
        if not job_header in request.headers:
            raise ValidationError('This is not a post deploy job request')
        if request.headers.get(job_header) != 'true':
            raise ValidationError('This is not a post deploy job request')
        
        call_command('migrate', '--noinput')
        call_command('createsu')
        return Response()
