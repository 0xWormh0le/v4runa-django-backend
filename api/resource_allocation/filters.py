from django.db.models import Q
from rest_framework import filters
from datetime import date, datetime, timedelta
import dateutil.parser


class ResourceAllocationFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """

    def filter_queryset(self, request, queryset, view):
        keyword = request.query_params.get('q', None)
        if keyword is not None:
            return queryset.filter(
                Q(assignee__user__first_name__icontains=keyword) |
                Q(assignee__user__last_name__icontains=keyword) |
                Q(job_number__icontains=keyword) |
                Q(location__street_address_2__icontains=keyword) |
                Q(location__city__icontains=keyword) |
                Q(location__state__icontains=keyword) |
                Q(location__zip_code__icontains=keyword) |
                Q(location__country__icontains=keyword)
            )
        else:
            return queryset
