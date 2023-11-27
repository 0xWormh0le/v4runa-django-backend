from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..user.permissions import CanAccessPumpReport
from pump.models import PumpCompareReport
from .serializers import (
    PumpReportSerializer,
    PumpReportCreateSerializer,
    PumpReportDetailSerializer
)


class ReportView(generics.ListCreateAPIView):
    """
    Gets pump comparison report list or creates a new one
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PumpReportSerializer
    pagination_class = None

    def create(self, request):
        serializer = PumpReportCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        pump_report = serializer.save()
        serializer = PumpReportSerializer(pump_report)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.is_admin:
            return PumpCompareReport.objects.all()
        else:
            return PumpCompareReport.objects.filter(user=self.request.user)


class ReportDetailView(generics.RetrieveAPIView):
    """
    Shows detailed report of pump comparison
    """
    
    serializer_class = PumpReportDetailSerializer
    queryset = PumpCompareReport.objects.all()
    
    def get_permissions(self):
        return (CanAccessPumpReport(id=self.kwargs['pk']), )
