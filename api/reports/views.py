from django.utils.decorators import method_decorator
from django.db.models import (Avg, Min, Max)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from datetime import timedelta
from common.filter_inspectors import SearchQueryFilterInspector
from ..user.permissions import CanAccessSensor
from utility.models import (
    MonthlyReport,
    Sensor,
    SensorDataRecord
)
from .serializers import (
    MonthlyReportSerializer,
)
from utility import constants as cs
from .helpers import weekly_report_data


class MonthlyReportListView(generics.ListAPIView):
    """
    Lists monthly reports for user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MonthlyReportSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return MonthlyReport.objects.all().order_by('-date')
        else:
            return MonthlyReport.objects.filter(water_utility=user.profile.water_utility).order_by('-date')

class WeeklyReportView(generics.GenericAPIView):
    """
    Shows weekly report for a sensor specified by parameter `sensorId`
    """

    def get_permissions(self):
        return (CanAccessSensor(id=self.request.query_params.get('sensor_id')),)

    def get(self, request):
        sensor_id = request.query_params.get('sensor_id')
        chemical = request.query_params.get('chemical')
        data = weekly_report_data(sensor_id, chemical)
        return Response(data)

