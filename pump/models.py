from django.db import models
from jsonfield import JSONField
from common.uploads import pump_compare_upload
from datetime import datetime
from django.utils.functional import cached_property


# Create your models here.

class PumpCompareReport(models.Model):
    """
    Represents pump comparison data
    """

    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255, help_text='Name')

    date_saved = models.DateTimeField(help_text='Date Saved', auto_now_add=True)

    started_from = models.DateTimeField(help_text='Started From', null=True)
    
    description = models.TextField(help_text='Description', null=True, blank=True)

    upload = models.FileField(upload_to=pump_compare_upload)

    @cached_property
    def data(self):
        data = self.upload.open('r').read()
        self.upload.close()
        return list(map(lambda x: x.split('\t'), data.splitlines()))

    def report(self, last_hours=24):
        channel_a_run_time = channel_b_run_time = 0
        channel_a_starts_number = channel_b_starts_number = 0
        channel_a_values = []
        channel_b_values = []

        start = len(self.data) - 3600 * last_hours
        data = self.data[start:]

        for item in data:
            if len(item) > 7:
                if int(item[1]) == 1:
                    channel_a_run_time += 1
                if int(item[5]) == 1:
                    channel_b_run_time += 1

                channel_a_starts_number += int(item[3])
                channel_b_starts_number += int(item[7])

                channel_a_values.append(item[0])
                channel_b_values.append(item[4])

        return {
            'pump_a': {
                'total_runtime_sec': channel_a_run_time,
                'num_starts': channel_a_starts_number,
                'values': channel_a_values
            },
            'pump_b': {
                'total_runtime_sec': channel_b_run_time,
                'num_starts': channel_b_starts_number,
                'values': channel_b_values
            },
            'avg_fill_time_min': 0,
            'total_gallons_pumped_day': 0,
            'start_from': datetime.timestamp(self.started_from) + start * 1000
        }
