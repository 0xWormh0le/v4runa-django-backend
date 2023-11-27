from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import pandas as pd
import math
from common.filter_inspectors import SearchQueryFilterInspector
from utility.models import (
    Sensor,
    SensorDataRecord,
)
from .serializers import (
    SensorDetailsSerializer,
    SensorWithDataRecordSerializer,
    SensorDataRecordSimpleSerializer,
    SensorDataRecordIntervalSerializer,
    SensorDataRecordListSerializer
)
from .filters import (
    SensorSearchFilterBackend,
    SensorDataRecordFilterBackend,
)

from .paginations import SensorDataRecordIntervalPagination
from ..user.permissions import CanAccessSensor


class SensorMixin(object):
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            sensors = Sensor.objects.all()
        else:
            sensors = Sensor.objects.filter(water_utility=user.profile.water_utility)
        return sensors.select_related('water_utility', 'water_utility__location').prefetch_related('alerts')


class ChemicalTypeMixin(object):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['chemical_type'] = self.kwargs['chemical']
        return context


class SensorDataRecordMixin(object):
    def get_permissions(self):
        return (CanAccessSensor(id=self.kwargs['pk']),)

    def get_queryset(self):
        chemical = self.kwargs.get('chemical', None)
        sensor_id = self.kwargs.get('pk')
        queryset = SensorDataRecord.objects.filter(sensor_id=sensor_id).order_by('-recorded_at')
        if chemical:
            # distinct prevents duplicate index error while reindexing panda time series
            return queryset.filter(value_type=chemical).distinct('recorded_at')
        return queryset


class SensorListView(SensorMixin, generics.ListAPIView):
    """
    Lists all the sensors.
    """

    serializer_class = SensorDetailsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None


@method_decorator(name='get', decorator=swagger_auto_schema(
    filter_inspectors=[SearchQueryFilterInspector]
))
class SensorSearchView(SensorMixin, generics.ListAPIView):
    """
    Search sensors by query parameter `q`.
    """ 
    serializer_class = SensorDetailsSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SensorSearchFilterBackend, )
    pagination_class = None


class SensorCurrentDataListView(SensorMixin, ChemicalTypeMixin, generics.ListAPIView):
    """
    Lists all the sensors with current chemical value.
    """

    serializer_class = SensorWithDataRecordSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().prefetch_related('records')


class SensorCurrentDataSearchView(SensorMixin, ChemicalTypeMixin, generics.ListAPIView):
    """
    Search sensors by query parameter `q` and return result with current chemical value.
    """

    serializer_class = SensorWithDataRecordSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SensorSearchFilterBackend, )
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().prefetch_related('records')


class SensorDataRecordListView(SensorDataRecordMixin, generics.ListAPIView):
    """
    Lists sensor data records between `from` and `to` dates every `interval` period.
    If `interval` is not specified, it defaults to an hour.
    If query params are not specified, it returns all records.
    """
    pagination_class = SensorDataRecordIntervalPagination
    filter_backends = (SensorDataRecordFilterBackend, )

    def get_serializer_class(self):
        if self.kwargs.get('interval') is None:
            return SensorDataRecordListSerializer
        else:
            return SensorDataRecordIntervalSerializer


    def formatSensorRecord(self, t, s):
        value = s[0]
        unit = s[1]
        if math.isnan(value):
            value = None
            unit = None
        return {
            'time': t,
            'value': value,
            'unit': unit
        }

    def get_data(self, queryset):
        self.start_date = None
        self.end_date = None

        interval = self.kwargs.get('interval')

        if interval is None:
            first = queryset.first()
            last = queryset.last()

            if first is not None:
                self.start_date = first.recorded_at
                self.end_date = last.recorded_at

            return queryset

        series = queryset.to_timeseries(index='recorded_at', fieldnames=('value', 'unit',))

        if len(series.index) > 0:
            self.start_date = series.index[-1]
            self.end_date = series.index[0]
            
            interval = '-{}'.format(interval)
            new_dt_index = pd.date_range(series.index[0], series.index[-1], freq=interval)
            series = series.reindex(new_dt_index)
            data = map(self.formatSensorRecord, series.index, series.values)
            return list(data)
        else:
            return []

    def paginate_queryset(self, queryset):
        qs = self.filter_queryset(self.get_queryset())
        return super().paginate_queryset(self.get_data(qs))

    def get_paginated_response(self, data):
        return super().get_paginated_response({
            'start_date': self.start_date,
            'end_date': self.end_date,
            'records': data
        })


class SensorDataRecordAllListView(SensorDataRecordMixin, generics.ListAPIView):
    """
    Lists all the sensor data records with pagination enabled.
    """

    serializer_class = SensorDataRecordSimpleSerializer


class SensorDataRecordLatestView(SensorDataRecordMixin, generics.RetrieveAPIView):
    """
    Get latest data record for specified by `chemical`.
    """

    serializer_class = SensorDataRecordSimpleSerializer

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset.first()
