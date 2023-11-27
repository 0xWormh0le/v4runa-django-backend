from rest_framework import serializers

from utility.models import (
    Technician,
)
from ..resource_allocation.serializers import ResourceAllocationSerializer
from ..user.serializers import UserSerializer


class TechnicianDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    current_job = ResourceAllocationSerializer()

    class Meta:
        model = Technician
        fields = (
            'id',
            'user',
            'hourly_rate',
            'preferred_job_type',
            'current_job',
        )
