from rest_framework import serializers
from django.conf import settings
from datetime import datetime
import dateutil.parser
from utility import constants as cs
from utility.models import Sensor, SensorDataRecord
from utility.signals import check_and_create_alert

value_types = {
    'p': cs.SENSOR_VALUE_PH,
    't': cs.SENSOR_VALUE_TURBIDITY,
    'w': cs.SENSOR_VALUE_WATER_TEMPERATURE,
    'a': cs.SENSOR_VALUE_AMBIENT_TEMPERATURE,
    'b': cs.SENSOR_VALUE_BATTERY_VOLTAGE,
    'g': cs.SENSOR_VALUE_GPS,
    'c': cs.CONTAMINATION_CHLORINE,
}

units = {
    'p': '',
    't': 'NTU',
    'w': '°C',
    'a': '°C',
    'b': 'V',
    'g': '',
    'c': 'ppm',
}

class IotSensorDataRecordSerializer(serializers.Serializer):
    coreid = serializers.CharField(max_length=256)
    api_key = serializers.CharField(max_length=256)
    event = serializers.CharField(max_length=16)
    data = serializers.CharField(max_length=256)
    published_at = serializers.DateTimeField()

    def validate_event(self, value):
        if not value in ('sensor', 'issue', 'function',):
            raise serializers.ValidationError("invalid")
        return value

    def validate_api_key(self, value):
        if settings.PARTICLE_API_KEY != value:
            raise serializers.ValidationError("invalid")
        return value

    def validate_coreid(self, value):
        sensor = Sensor.objects.filter(device_id=value).first()
        if sensor is None:
            raise serializers.ValidationError("invalid")
        return sensor

    def validate_published_at(self, value):
        return datetime.fromtimestamp(round(value.timestamp() / 15) * 15)

    def create(self, validated_data):
        data = validated_data['data'].split(';')
        time = validated_data['published_at']
        event = validated_data['event']
        device = validated_data['coreid']
        
        if event == 'sensor':
            return self.deviceEvent(device, data, time)
        elif event == 'issue':
            return self.issueEvent(device, data, time)
        elif event == 'function':
            return self.functionEvent(device, data, time)
        else:
            return True

    def deviceEvent(self, device, data, time):
        records = []
        chemical_records = []

        for d in data:
            if len(d) > 2:
                c = d[0]
                if all([c in value_types, d[1] == ':']):
                    value_type = value_types[c]
                    value = d[2:]
                    record = SensorDataRecord(
                        sensor=device,
                        value_type=value_type,
                        value=float(value) if value_type != cs.SENSOR_VALUE_GPS else None,
                        value_str=None if value_type != cs.SENSOR_VALUE_GPS else value,
                        unit=units[c],
                        recorded_at=time
                    )

                    records.append(record)

                    if value_type != cs.SENSOR_VALUE_GPS:
                        chemical_records.append(record)

        SensorDataRecord.objects.bulk_create(records)

        for record in chemical_records:
            check_and_create_alert(record)

        return True

    def issueEvent(self, device, data, time):
        for d in data:
            if d == 'DOOR OPEN':
                pass
        return True

    def functionEvent(self, device, data, time):
        return True
