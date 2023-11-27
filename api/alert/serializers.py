from rest_framework import serializers

from utility.models import (
    Alert,
)
from ..sensor.serializers import (
    SensorDetailsSerializer,
    SensorSimpleSerializer,
    SensorDataRecordSimpleSerializer
)

class AlertDetailsSerializer(serializers.ModelSerializer):
    sensor = SensorDetailsSerializer()
    sensor_data_record = SensorDataRecordSimpleSerializer()

    class Meta:
        model = Alert
        fields = (
            'id',
            'alert_type',
            'reported_at',
            'message',
            'status',
            'sensor',
            'sensor_data_record',
        )


class AlertSimpleSerializer(serializers.ModelSerializer):
    sensor = SensorSimpleSerializer()

    class Meta:
        model = Alert
        fields = (
            'id',
            'alert_type',
            'reported_at',
            'message',
            'status',
            'sensor',
            'city'
        )
        read_only_fields = ('city',)
