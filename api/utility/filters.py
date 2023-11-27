from django.db.models import Q
from rest_framework import filters
from datetime import date
import dateutil.parser


class WaterUtilityAutoCompleteFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """
    def filter_queryset(self, request, queryset, view):
        keyword = request.query_params.get('q', None)
        if keyword is not None:
            return queryset.filter(
                Q(name__icontains=keyword) | Q(water_system_id=keyword)
            )
        else:
            return queryset


class WaterUtilityFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """
    def filter_queryset(self, request, queryset, view):
        keyword = request.query_params.get('q', None)
        if keyword is not None:
            return queryset.filter(
                Q(name__icontains=keyword) |
                Q(water_system_id=keyword) |
                Q(location__street_address_1__icontains=keyword) |
                Q(location__street_address_2__icontains=keyword) |
                Q(location__city__icontains=keyword) |
                Q(location__state__icontains=keyword) |
                Q(location__zip_code__icontains=keyword) |
                Q(location__country__icontains=keyword)
            )
        else:
            return queryset


class WaterQualityFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """
    def filter_queryset(self, request, queryset, view):
        str_from = request.query_params.get('from', None)
        if str_from is not None:
            dt_from = dateutil.parser.parse(str_from)
        else:
            dt_from = date.today()
        queryset = queryset.filter(date__gte=dt_from)

        str_to = request.query_params.get('to', None)
        if str_to is not None:
            dt_to = dateutil.parser.parse(str_to)
            queryset = queryset.filter(date__lte=dt_to)

        return queryset


class SensorFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with <pk> parameter
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(water_utility_id=view.kwargs['pk'])
