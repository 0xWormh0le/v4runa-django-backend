from django.db.models import Q
from rest_framework import filters
from datetime import date, datetime, timedelta
import dateutil.parser


class TechnicianFilterBackend(filters.BaseFilterBackend):
    """
    Filters queryset with query parameter
    """

    def filter_queryset(self, request, queryset, view):
        keyword = request.query_params.get('q', None)
        if keyword is not None:
            return queryset.filter(
                Q(user__first_name__icontains=keyword) |
                Q(user__last_name__icontains=keyword)
            )
        else:
            return queryset
