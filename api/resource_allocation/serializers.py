from rest_framework import serializers

from utility.models import (
    ResourceAllocation,
    ResourceAllocationCalendar,
    Technician,
)
from ..geo.serializers import AddressSerializer
from ..user.serializers import UserSerializer

class TechnicianSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Technician
        fields = (
            'id',
            'user',
            'hourly_rate',
            'preferred_job_type',
        )


class ResourceAllocationCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceAllocationCalendar
        fields = (
            'date',
        )


class ResourceAllocationSerializer(serializers.ModelSerializer):
    assignee = TechnicianSerializer()
    location = AddressSerializer()

    class Meta:
        model = ResourceAllocation
        fields = (
            'id',
            'job_number',
            'assignee',
            'alert',
            'job_type',
            'department',
            'start_date',
            'closing_date',
            'location',
            'salary',
        )
