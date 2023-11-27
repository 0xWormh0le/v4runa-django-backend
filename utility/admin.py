from django.contrib import admin
from django.urls import path

from common.admin import admin_site
from .models import (
    Alert,
    AssetFinance,
    ResourceAllocation,
    ResourceAllocationCalendar,
    Sensor,
    SensorDataRecord,
    Technician,
    WaterQuality,
    WaterUtility,
    Contact,
    AnnualOperatingPeriod,
    ServiceConnection,
    ServiceArea,
    CertificationRequirement,
    Facility,
    FacilityProcessDetail,
    FacilityFlow,
    Sale,
    TcrSample,
    TcrSampleSchedule,
    TcrSampleResult,
    NonTcrSample,
    NonTcrSampleSchedule,
    Violation,
    SiteVisit,
    SiteVisitDetail,
    MonthlyReport,
    RawWater,
)
from .views import (
    AssetFinanceImportView,
    WaterUtilityImportView,
    WaterQualityImportView,
    SensorImportView,
    SensorDataRecordPopulateTestRecordsView,
    TechnicianImportView,
    AlertAllocateResourceView,
)


class ContactInline(admin.TabularInline):
    model = Contact
    autocomplete_fields = ('location', )


class AnnualOperatingPeriodInline(admin.TabularInline):
    model = AnnualOperatingPeriod


class ServiceConnectionInline(admin.TabularInline):
    model = ServiceConnection


class ServiceAreaInline(admin.TabularInline):
    model = ServiceArea


class CertificationRequirementInline(admin.TabularInline):
    model = CertificationRequirement


class FacilityInline(admin.TabularInline):
    model = Facility


class FacilityProcessDetailInline(admin.TabularInline):
    model = FacilityProcessDetail


class FacilityFlowInline(admin.TabularInline):
    model = FacilityFlow


class TcrSampleInline(admin.TabularInline):
    model = TcrSample


class TcrSampleScheduleInline(admin.TabularInline):
    model = TcrSampleSchedule


class TcrSampleResultInline(admin.TabularInline):
    model = TcrSampleResult


class NonTcrSampleInline(admin.TabularInline):
    model = NonTcrSample


class NonTcrSampleScheduleInline(admin.TabularInline):
    model = NonTcrSampleSchedule


class ViolationInline(admin.TabularInline):
    model = Violation


class SiteVisitInline(admin.TabularInline):
    model = SiteVisit


class SiteVisitDetailInline(admin.TabularInline):
    model = SiteVisitDetail

class SensorInline(admin.TabularInline):
    model = Sensor
    autocomplete_fields = ('location', )


class WaterUtilityMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(WaterUtilityImportView.as_view()),
                name='utility_waterutility_import'
            ),
        ]
        return custom_urls + urls


class AssetFinanceMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(AssetFinanceImportView.as_view()),
                name='utility_assetfinance_import'
            ),
        ]
        return custom_urls + urls


class WaterQualityMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(WaterQualityImportView.as_view()),
                name='utility_waterquality_import'
            ),
        ]
        return custom_urls + urls


class SensorMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(SensorImportView.as_view()),
                name='utility_sensor_import'
            ),
        ]
        return custom_urls + urls


class SensorDataRecordMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'populate-test-records/',
                self.admin_site.admin_view(SensorDataRecordPopulateTestRecordsView.as_view()),
                name='utility_sensordatarecord_populatetestrecords'
            ),
        ]
        return custom_urls + urls


class TechnicianMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'import/',
                self.admin_site.admin_view(TechnicianImportView.as_view()),
                name='utility_technician_import'
            ),
        ]
        return custom_urls + urls


class AlertMixin:
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'create-allocations/',
                self.admin_site.admin_view(AlertAllocateResourceView.as_view()),
                name='utility_alert_createallocations'
            ),
        ]
        return custom_urls + urls


@admin.register(WaterUtility, site=admin_site)
class WaterUtilityAdmin(WaterUtilityMixin, admin.ModelAdmin):
    list_display = ('water_system_id', 'name', 'location', 'water_system_type')
    autocomplete_fields = ('location', )
    search_fields = (
        'water_system_id',
        'name',
        'location__street_address_1',
        'location__city',
        'location__state',
        'location__zip_code',
        'location__country',
    )
    inlines = (
        SensorInline,
        ContactInline,
        AnnualOperatingPeriodInline,
        ServiceConnectionInline,
        ServiceAreaInline,
        CertificationRequirementInline,
        FacilityInline,
        ViolationInline,
        SiteVisitInline,
    )
    list_filter = (
        'water_system_type',
        'primary_water_source_type',
    )


@admin.register(AssetFinance, site=admin_site)
class AssetFinanceAdmin(AssetFinanceMixin, admin.ModelAdmin):
    list_display = ('water_utility', 'asset_name', )


@admin.register(WaterQuality, site=admin_site)
class WaterQualityAdmin(WaterQualityMixin, admin.ModelAdmin):
    autocomplete_fields = ('water_utility', )
    list_display = ('water_utility', 'date', )


@admin.register(Sensor, site=admin_site)
class SensorAdmin(SensorMixin, admin.ModelAdmin):
    autocomplete_fields = ('water_utility', 'location', )
    list_display = ('device_id', 'water_utility', 'location', )
    search_fields = ('device_id', 'location', )


@admin.register(SensorDataRecord, site=admin_site)
class SensorDataRecordAdmin(SensorDataRecordMixin, admin.ModelAdmin):
    autocomplete_fields = ('sensor',)
    list_display = ('sensor', 'recorded_at', 'value_type', 'value', )
    search_fields = ('value_type', 'recorded_at', 'sensor__device_id', 'value',)
    list_filter = ('value_type',)


@admin.register(Alert, site=admin_site)
class AlertAdmin(AlertMixin, admin.ModelAdmin):
    autocomplete_fields = ('sensor', 'sensor_data_record', )
    list_display = ('sensor_data_record', 'alert_type', 'reported_at', 'message', 'status', )
    search_fields = ('message', 'reported_at', 'sensor__device_id',)
    list_filter = ('alert_type', 'status',)


@admin.register(Technician, site=admin_site)
class TechnicianAdmin(TechnicianMixin, admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'preferred_job_type', )


@admin.register(ResourceAllocation, site=admin_site)
class ResourceAllocationAdmin(admin.ModelAdmin):
    list_display = ('job_number', 'assignee', 'alert', 'location', 'job_type', 'department', 'closing_date', )
    autocomplete_fields = ('location', )


@admin.register(ResourceAllocationCalendar, site=admin_site)
class ResourceAllocationCalendarAdmin(admin.ModelAdmin):
    list_display = ('allocation', 'date', )

@admin.register(Contact, site=admin_site)
class ContactAdmin(admin.ModelAdmin):
    autocomplete_fields = ('water_utility', 'location', )

@admin.register(AnnualOperatingPeriod, site=admin_site)
class AnnualOperatingPeriodAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceConnection, site=admin_site)
class ServiceConnectionAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceArea, site=admin_site)
class ServiceAreaAdmin(admin.ModelAdmin):
    pass

@admin.register(CertificationRequirement, site=admin_site)
class CertificationRequirementAdmin(admin.ModelAdmin):
    pass

@admin.register(Facility, site=admin_site)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'water_utility')
    inlines = [
        FacilityProcessDetailInline,
    ]

@admin.register(FacilityProcessDetail, site=admin_site)
class FacilityProcessDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(FacilityFlow, site=admin_site)
class FacilityFlowAdmin(admin.ModelAdmin):
    pass

@admin.register(Sale, site=admin_site)
class SaleAdmin(admin.ModelAdmin):
    pass

@admin.register(TcrSample, site=admin_site)
class TcrSampleAdmin(admin.ModelAdmin):
    inlines = [
        TcrSampleResultInline
    ]

@admin.register(TcrSampleSchedule, site=admin_site)
class TcrSampleScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(TcrSampleResult, site=admin_site)
class TcrSampleResultAdmin(admin.ModelAdmin):
    pass

@admin.register(NonTcrSample, site=admin_site)
class NonTcrSampleAdmin(admin.ModelAdmin):
    pass

@admin.register(NonTcrSampleSchedule, site=admin_site)
class NonTcrSampleScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Violation, site=admin_site)
class ViolationAdmin(admin.ModelAdmin):
    pass

@admin.register(SiteVisit, site=admin_site)
class SiteVisitAdmin(admin.ModelAdmin):
    inlines = [
        SiteVisitDetailInline,
    ]

@admin.register(SiteVisitDetail, site=admin_site)
class SiteVisitDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(MonthlyReport, site=admin_site)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'water_utility', )
    search_fields = ('water_utility__name', 'water_utility__water_system_id',)
    autocomplete_fields = ('water_utility', )

@admin.register(RawWater, site=admin_site)
class RawWater(admin.ModelAdmin):
    pass
