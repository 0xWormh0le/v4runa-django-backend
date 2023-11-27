from rest_framework import viewsets

from iccr.models import TempReport
from .serializers import TempReportSerializer
from ..user.permissions import IsAdminOrGeneralManager


class TempReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    pagination_class = None
    serializer_class = TempReportSerializer
    queryset = TempReport.objects.all()

    def get_permissions(self):
        if self.action == self.action_map['get']:
            return []
        return [IsAdminOrGeneralManager()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
