from rest_framework import serializers
from rest_framework.reverse import reverse
from utility.models import (
    MonthlyReport
)


class MonthlyReportSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, monthly_report):
        """
        Get download url of monthly report.
        """
        request = self.context['request']
        base_url = reverse('monthly-report-download', args=[monthly_report.pk], request=request)
        return '{}?auth={}'.format(base_url, request.auth.token.decode('utf-8'))

    class Meta:
        model = MonthlyReport
        fields = (
            'id',
            'water_utility',
            'date',
            'url',
            'title',
            'size',
        )
        read_only_fields = ('url', 'title', 'size',)
