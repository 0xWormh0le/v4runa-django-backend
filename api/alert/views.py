from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.filter_inspectors import SearchQueryFilterInspector
from utility.models import (
    Alert,
)
from .serializers import (
    AlertSimpleSerializer,
)
from .filters import (
    AlertSearchFilterBackend,
)

from ..user.permissions import CanAccessSensor

from utility import constants as cs


class AlertListView(generics.ListAPIView):
    """
    Lists all the alerts.
    """

    serializer_class = AlertSimpleSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Alert.objects.all().order_by('-reported_at').select_related(
        'sensor',
        'sensor__water_utility',
        'sensor__water_utility__location',
        'sensor_data_record',
    )


@method_decorator(name='get', decorator=swagger_auto_schema(
    filter_inspectors=[SearchQueryFilterInspector]
))
class AlertSearchView(generics.ListAPIView):
    """
    Search sensors by query parameter 'q'.
    """ 
    serializer_class = AlertSimpleSerializer
    filter_backends = (AlertSearchFilterBackend, )
    pagination_class = None

    def get_permissions(self):
        sensor_id = self.kwargs.get('sensor_id', None)
        if sensor_id is None:
            return (IsAuthenticated(),)
        else:
            return (CanAccessSensor(id=self.kwargs['sensor_id']),)

    def get_queryset(self):
        sensor_id = self.kwargs.get('sensor_id', None)
        queryset = Alert.objects.filter(status=cs.ALERT_STATUS_IN_PROCESS) \
            .order_by('-reported_at') \
            .select_related(
                'sensor_data_record',
                'sensor_data_record__sensor',
                'sensor_data_record__sensor__water_utility',
            )

        if sensor_id is None:
            user = self.request.user
            if not user.is_admin and not user.is_general_manager:
                queryset = queryset.filter(sensor_data_record__sensor__water_utility=user.profile.water_utility)
        else:
            queryset = queryset.filter(sensor_data_record__sensor_id=sensor_id)

        return queryset
