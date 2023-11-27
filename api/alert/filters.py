from django.db.models import Q
from rest_framework import filters


class AlertSearchFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """

    def filter_queryset(self, request, queryset, view):
        keyword = request.query_params.get('q', None)
        if keyword is not None:
            return queryset.filter(
                Q(sensor__device_id__icontains=keyword) |
                Q(sensor__water_utility__name__icontains=keyword) |
                Q(sensor__water_utility__location__street_address_2__icontains=keyword) |
                Q(sensor__water_utility__location__city__icontains=keyword) |
                Q(sensor__water_utility__location__state__icontains=keyword) |
                Q(sensor__water_utility__location__zip_code__icontains=keyword) |
                Q(sensor__water_utility__location__country__icontains=keyword)
            )
        else:
            return queryset
