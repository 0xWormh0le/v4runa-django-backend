from rest_framework import viewsets
from rest_framework import serializers as drf_serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utility.constants import (
    WATER_SYSTEM_TYPE_CHOICES,
    WATER_SOURCE_TYPE_CHOICES,
    WATER_REGULATIONS,
)

class SettingsViewSet(viewsets.ViewSet):
    """
    API endpoint that retrieves platform settings.
    """
    serializer_class = drf_serializers.Serializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        data = {
            'water_regulations': self.water_regulations(request).data,
            'water_source_types': self.water_source_types(request).data,
            'water_system_types': self.water_system_types(request).data,
        }
        return Response(data)

    @action(detail=False, url_path='water-regulations')
    def water_regulations(self, request):
        data = dict(WATER_REGULATIONS)
        return Response(data)

    @action(detail=False, url_path='water-system-types')
    def water_system_types(self, request):
        data = [{
            'id': item[0],
            'name': item[1],
        } for item in WATER_SYSTEM_TYPE_CHOICES]
        return Response(data)

    @action(detail=False, url_path='water-source-types')
    def water_source_types(self, request):
        data = [{
            'id': item[0],
            'name': item[1],
        } for item in WATER_SOURCE_TYPE_CHOICES]
        return Response(data)
