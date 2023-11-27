from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django import forms

from common.admin import admin_site
from .models import (
    AssetFinance,
    WaterQuality,
    WaterUtility,
    Sensor,
    SensorDataRecord,
    Technician,
    ResourceAllocation,
)
from .forms import (
    AssetFinanceImportForm,
    WaterQualityImportForm,
    WaterUtilityImportForm,
    SensorImportForm,
    SensorPopulateTestRecordsForm,
    TechnicianImportForm,
    AlertAllocateResourceForm,
)
from .importers import (
    import_asset_finance_data,
    import_water_quality_history,
    import_water_utilities,
    import_sensors,
    import_technicians,
)
from .management.commands.populate_test_sensor_data_records import populate_test_sensor_record_data
from .management.commands.allocate_alerts_to_technicians import allocate_alerts_to_technicians


class WaterUtilityImportView(FormView):
    template_name = 'water_utility/import.html'
    form_class = WaterUtilityImportForm
    model = WaterUtility

    def get_success_url(self):
        return reverse('admin:utility_waterutility_changelist')

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'import': True,
            'has_view_permission': True,
            'has_file_field': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_water_utilities(form.cleaned_data['csv'])
            messages.success(request, 'Water Utilities have been imported.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AssetFinanceImportView(FormView):
    template_name = 'asset_finance/import.html'
    form_class = AssetFinanceImportForm
    model = AssetFinance

    def get_success_url(self):
        return reverse('admin:utility_assetfinance_changelist')

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'import': True,
            'has_view_permission': True,
            'has_file_field': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_asset_finance_data(form.cleaned_data['csv'])
            messages.success(request, 'Asset and finance data has been imported.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class WaterQualityImportView(FormView):
    template_name = 'water_quality/import.html'
    form_class = WaterQualityImportForm
    model = WaterQuality

    def get_success_url(self):
        return reverse('admin:utility_waterquality_changelist')

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'import': True,
            'has_view_permission': True,
            'has_file_field': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_water_quality_history(form.cleaned_data['csv'])
            messages.success(request, 'Water quality history has been imported.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SensorImportView(FormView):
    template_name = 'sensor/import.html'
    form_class = SensorImportForm
    model = Sensor

    def get_success_url(self):
        return reverse('admin:utility_sensor_changelist')

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'import': True,
            'has_view_permission': True,
            'has_file_field': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_sensors(form.cleaned_data['csv'])
            messages.success(request, 'Sensors have been imported.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SensorDataRecordPopulateTestRecordsView(FormView):
    template_name = 'sensor_data_record/populate_test_records.html'
    form_class = SensorPopulateTestRecordsForm
    model = SensorDataRecord

    def get_success_url(self):
        return reverse('admin:utility_sensordatarecord_changelist')

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        js = [
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
            'core.js',
            'admin/RelatedObjectLookups.js',
            'actions%s.js' % extra,
            'urlify.js',
            'prepopulate%s.js' % extra,
            'vendor/xregexp/xregexp%s.js' % extra,
        ]
        return forms.Media(js=['admin/js/%s' % url for url in js])

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'media': self.media,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            populate_test_sensor_record_data(start_date, end_date)
            messages.success(request, 'Test sensor data records have been populated.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TechnicianImportView(FormView):
    template_name = 'technician/import.html'
    form_class = TechnicianImportForm
    model = Technician

    def get_success_url(self):
        return reverse('admin:utility_technician_changelist')

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'import': True,
            'has_view_permission': True,
            'has_file_field': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_technicians(form.cleaned_data['csv'])
            messages.success(request, 'Technicians have been imported.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AlertAllocateResourceView(FormView):
    template_name = 'alert/allocate_alerts_to_technicians.html'
    form_class = AlertAllocateResourceForm
    model = ResourceAllocation

    def get_success_url(self):
        return reverse('admin:utility_resourceallocation_changelist')

    def get_context_data(self, **kwargs):
        context = {
            **admin_site.each_context(self.request),
            **super().get_context_data(**kwargs),
            'opts': self.model._meta,
            'import': True,
            'has_view_permission': True,
            'has_file_field': True,
        }
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            allocate_alerts_to_technicians()
            messages.success(request, 'Allocations have been created for new alerts.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
