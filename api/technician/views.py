from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.filter_inspectors import SearchQueryFilterInspector
from utility.models import (
    Technician,
    ResourceAllocation,
)
from .serializers import (
    TechnicianDetailsSerializer,
)
from .filters import (
    TechnicianFilterBackend,
)


class TechnicianListView(generics.ListAPIView):
    """
    Lists all the resource allocations.
    """

    serializer_class = TechnicianDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Technician.objects.all()
    pagination_class = None


@method_decorator(name='get', decorator=swagger_auto_schema(
    filter_inspectors=[SearchQueryFilterInspector]
))
class TechnicianSearchView(generics.ListAPIView):
    """
    Search resource allocations by query parameter 'q'.
    """
    serializer_class = TechnicianDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Technician.objects.all()
    filter_backends = (TechnicianFilterBackend, )
    pagination_class = None


class TechnicianDetailsView(generics.RetrieveAPIView):
    """
    Get technician details that belongs to the technician specified by `<pk>`.
    """
    serializer_class = TechnicianDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Technician.objects.all()
