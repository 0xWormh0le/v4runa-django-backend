from rest_framework import serializers
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from pump.models import PumpCompareReport
from .helpers import parse_report_upload


class PumpReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PumpCompareReport
        fields = ('id', 'name', 'date_saved', 'description', )


class PumpReportCreateSerializer(serializers.ModelSerializer):
    data = serializers.CharField()

    class Meta:
        model = PumpCompareReport
        fields = ('id', 'name', 'data', 'started_from', 'description', )

    def validate_data(self, value):
        return value

    def create(self, validated_data):
        report = PumpCompareReport(
            user=self.context['request'].user,
            name=validated_data['name'],
            started_from=validated_data['started_from'],
            description=validated_data['description']
        )
        report.upload.save(
            name=validated_data['name'],
            content=ContentFile(bytearray(validated_data['data'], 'utf8'))
        )
        report.save()
        return report


class PumpReportDetailSerializer(serializers.ModelSerializer):
    report = serializers.SerializerMethodField()

    def get_report(self, pump_report):
        last_hours = self.context['request'].query_params.get('last-hours')
        if last_hours is None:
            return pump_report.report()
        else:
            return pump_report.report(int(last_hours))

    class Meta:
        model = PumpCompareReport
        fields = ('id', 'started_from', 'report', )


