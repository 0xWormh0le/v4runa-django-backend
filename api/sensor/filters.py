from django.db.models import Q
from rest_framework import filters
from datetime import date, datetime, timedelta
import dateutil.parser


class SensorSearchFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """

    def filter_queryset(self, request, queryset, view):
        keyword = request.query_params.get('q', None)
        if keyword is not None:
            return queryset.filter(
                Q(device_id__icontains=keyword) |
                Q(water_utility__name__icontains=keyword) |
                Q(location__street_address_1__icontains=keyword) |
                Q(location__street_address_2__icontains=keyword) |
                Q(location__city__icontains=keyword) |
                Q(location__state__icontains=keyword) |
                Q(location__zip_code__icontains=keyword) |
                Q(location__country__icontains=keyword)
            )
        else:
            return queryset


class SensorDataRecordFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with <pk> parameter
    """
    def filter_queryset(self, request, queryset, view):
        str_from = request.query_params.get('from', None)
        str_to = request.query_params.get('to', None)
        
        if str_from:
            dt_from = dateutil.parser.parse(str_from)
            queryset = queryset.filter(recorded_at__gte=dt_from)

        if str_to:
            dt_to = dateutil.parser.parse(str_to)
            queryset = queryset.filter(recorded_at__lte=dt_to)

        return queryset
