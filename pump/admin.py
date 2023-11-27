from django.contrib import admin
from common.admin import admin_site
from .models import PumpCompareReport

# Register your models here.

@admin.register(PumpCompareReport, site=admin_site)
class PumpCompareAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', )
