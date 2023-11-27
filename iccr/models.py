from django.db import models
from django.db.models.deletion import CASCADE
from jsonfield import JSONField


class TempReport(models.Model):
    report_json = JSONField(
        default=None,
        null=True,
        blank=True,
    )
    user = models.ForeignKey('user.User', related_name='temp_reports', on_delete=CASCADE)
