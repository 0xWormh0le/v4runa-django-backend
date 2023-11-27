from rest_framework import serializers

from utility.models import (
    Sensor,
    SensorDataRecord,
)
from ..utility.serializers import WaterUtilitySerializer
from ..geo.serializers import AddressSerializer


class SensorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = (
            'id',
            'device_id',
            'water_utility'
        )


class SensorDetailsSerializer(serializers.ModelSerializer):
    water_utility = WaterUtilitySerializer()
    location = AddressSerializer()

    class Meta:
        model = Sensor
        fields = (
            'id',
            'device_id',
            'water_utility',
            'location',
            'has_issue',
        )
        read_only_fields = ('has_issue',)


class SensorWithDataRecordSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    location = AddressSerializer()

    def get_value(self, sensor):
        """
        Get sensor's chemical record value for chemical type
        """
        chemical_type = self.context.get('chemical_type')
        value = sensor.records.filter(value_type=chemical_type).order_by('-recorded_at').first()
        return SensorDataRecordSimpleSerializer(value).data
    
    class Meta:
        model = Sensor
        fields = (
            'id',
            'device_id',
            'location',
            'has_issue',
            'value',
        )
        read_only_fields = ('has_issue', 'value',)


class SensorDataRecordSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDataRecord
        fields = (
            'id',
            'sensor',
            'recorded_at',
            'value',
            'value_type',
            'unit',
        )


class SensorDataRecordIntervalSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    value = serializers.FloatField()
    unit = serializers.CharField(max_length=20)


class SensorDataRecordListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(source='recorded_at', read_only=True)
    value = serializers.FloatField()
    unit = serializers.CharField(max_length=20)

    class Meta:
        model = SensorDataRecord
        fields = (
            'id',
            'time',
            'value',
            'unit',
        )


class SensorDataRecordDetailsSerializer(serializers.ModelSerializer):
    sensor = SensorDetailsSerializer()

    class Meta:
        model = SensorDataRecord
        fields = (
            'id',
            'sensor',
            'recorded_at',
            'value',
            'value_type',
        )
