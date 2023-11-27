from django.db import models

from common.utils import get_next_job_number


class ResourceAllocationManager(models.Manager):
    def get_new_job_number(self):
        last_job = super().get_queryset().order_by('-job_number').first()
        if last_job:
            return get_next_job_number(last_job.job_number)
        else:
            return get_next_job_number()
