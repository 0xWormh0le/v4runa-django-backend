from django.contrib import admin
from django.urls import path

from common.admin import admin_site
from .models import TempReport
from .views import TempReportImportView


class TempReportMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(TempReportImportView.as_view()),
                name='iccr_tempreport_import'
            ),
        ]
        return custom_urls + urls


@admin.register(TempReport, site=admin_site)
class TempReportAdmin(TempReportMixin, admin.ModelAdmin):
    model = TempReport
    search_fields = ('report_json', )
