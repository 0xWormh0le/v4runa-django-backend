from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django import forms

from common.admin import admin_site
from .models import TempReport
from .forms import TempReportImportForm
from .importers import import_temp_report_from_json


class TempReportImportView(FormView):
    template_name = 'temp_report/import.html'
    form_class = TempReportImportForm
    model = TempReport

    def get_success_url(self):
        return reverse('admin:iccr_tempreport_changelist')

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
            import_temp_report_from_json(form.cleaned_data['json'], request.user)
            messages.success(request, 'Legacy Report data has been imported.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
