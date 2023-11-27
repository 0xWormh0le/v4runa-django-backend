from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from common.filter_inspectors import SearchQueryFilterInspector
from utility.models import (
    AssetFinance,
    WaterUtility,
    WaterQuality,
    Sensor,
)
from .serializers import (
    AssetFinanceSerializer,
    WaterQualitySerializer,
    WaterUtilitySerializer,
    WaterUtilityAutoCompleteSerializer,
)
from .filters import (
    WaterQualityFilterBackend,
    WaterUtilityFilterBackend,
    WaterUtilityAutoCompleteFilterBackend,
    SensorFilterBackend,
)
from ..sensor.serializers import (
    SensorDetailsSerializer,
)

from ..user.permissions import CanAccessWaterUtility


class WaterUtilityAutoCompleteListView(generics.ListAPIView):
    """
    Lists all water utilities by query parameter `q` with pagination enabled.
    """

    serializer_class = WaterUtilityAutoCompleteSerializer
    filter_backends = (WaterUtilityAutoCompleteFilterBackend, )
    queryset = WaterUtility.objects.all()


class WaterUtilityListView(generics.ListAPIView):
    """
    Lists all water utilities with pagination enabled.
    """

    serializer_class = WaterUtilitySerializer
    permission_classes = (IsAuthenticated,)
    queryset = WaterUtility.objects.all().select_related('location')


class WaterUtilityDetailsView(generics.RetrieveAPIView):
    """
    Get water utility details that belongs to the water utility specified by `<pk>`.
    """
    def get_permissions(self):
        return (CanAccessWaterUtility(id=self.kwargs['pk']),)

    serializer_class = WaterUtilitySerializer
    permission_classes = (IsAuthenticated,)
    queryset = WaterUtility.objects.all()


@method_decorator(name='get', decorator=swagger_auto_schema(
    filter_inspectors=[SearchQueryFilterInspector]
))
class WaterUtilitySearchView(generics.ListAPIView):
    """
    Lists search result of water utilities specified by query parameter `q`.
    """

    serializer_class = WaterUtilitySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (WaterUtilityFilterBackend, )
    queryset = WaterUtility.objects.all().select_related('location')
    pagination_class = None


class AssetFinanceListView(generics.ListAPIView):
    """
    Lists assets and finances of a specific water utility.
    """

    serializer_class = AssetFinanceSerializer
    permission_classes = (IsAuthenticated,)
    queryset = AssetFinance.objects.all()
    pagination_class = None


class WaterQualityHistoryView(generics.ListAPIView):
    """
    Lists water quality history data between `from` and `to` dates.
    If query params are not specified, it returns the history data of today.
    """

    serializer_class = WaterQualitySerializer
    permission_classes = (IsAuthenticated,)
    queryset = WaterQuality.objects.all()
    filter_backends = (WaterQualityFilterBackend, )
    pagination_class = None


class WaterQualityAllHistoryView(generics.ListAPIView):
    """
    Lists all the history data of water quality with pagination enabled.
    """

    serializer_class = WaterQualitySerializer
    permission_classes = (IsAuthenticated,)
    queryset = WaterQuality.objects.all()


class SensorListView(generics.ListAPIView):
    """
    Lists all the sensors that belongs to the water utility specified by `<pk>`.
    """

    serializer_class = SensorDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Sensor.objects.all()
    pagination_class = None
    filter_backends = (SensorFilterBackend, )
