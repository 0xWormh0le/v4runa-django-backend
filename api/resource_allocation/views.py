from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.filter_inspectors import SearchQueryFilterInspector
from utility.models import (
    ResourceAllocation,
    ResourceAllocationCalendar,
)
from .serializers import (
    ResourceAllocationSerializer,
    ResourceAllocationCalendarSerializer,
)
from .filters import (
    ResourceAllocationFilterBackend,
)


class ResourceAllocationListView(generics.ListAPIView):
    """
    Lists all the resource allocations.
    """

    serializer_class = ResourceAllocationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ResourceAllocation.objects.all().order_by('job_number')
    pagination_class = None


@method_decorator(name='get', decorator=swagger_auto_schema(
    filter_inspectors=[SearchQueryFilterInspector]
))
class ResourceAllocationSearchView(generics.ListAPIView):
    """
    Search resource allocations by query parameter 'q'.
    """
    serializer_class = ResourceAllocationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ResourceAllocation.objects.all().order_by('job_number')
    filter_backends = (ResourceAllocationFilterBackend, )
    pagination_class = None


class ResourceAllocationCalendarView(generics.ListAPIView):
    serializer_class = ResourceAllocationCalendarSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        pk = self.kwargs['pk']
        return ResourceAllocationCalendar.objects.filter(allocation=pk).order_by('date')
