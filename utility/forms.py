from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.templatetags.static import static


class WaterUtilityImportForm(forms.Form):
    csv = forms.FileField(
        label='CSV File',
        help_text='Choose a CSV file that contains water utility information. <a href="{}" download>Click Here</a> to download a sample CSV file.'.format(static('sample_downloads/water-utility.csv')),
        required=True,
    )


class AssetFinanceImportForm(forms.Form):
    csv = forms.FileField(
        label='CSV File',
        help_text='Choose a CSV file that contains asset and finance data. <a href="{}" download>Click Here</a> to download a sample CSV file.'.format(static('sample_downloads/asset-finance.csv')),
        required=True,
    )


class WaterQualityImportForm(forms.Form):
    csv = forms.FileField(
        label='CSV File',
        help_text='Choose a CSV file that contains water quality information. <a href="{}" download>Click Here</a> to download a sample CSV file.'.format(static('sample_downloads/water-quality.csv')),
        required=True,
    )


class SensorImportForm(forms.Form):
    csv = forms.FileField(
        label='CSV File',
        help_text='Choose a CSV file that contains sensor information. <a href="{}" download>Click Here</a> to download a sample CSV file.'.format(static('sample_downloads/sensor.csv')),
        required=True,
    )


class TechnicianImportForm(forms.Form):
    csv = forms.FileField(
        label='CSV File',
        help_text='Choose a CSV file that contains sensor information. <a href="{}" download>Click Here</a> to download a sample CSV file.'.format(static('sample_downloads/technician.csv')),
        required=True,
    )


class SensorPopulateTestRecordsForm(forms.Form):
    start_date = forms.SplitDateTimeField(
        label='Start Date',
        help_text='Choose start date to populate test records from.',
        required=True,
        widget=AdminSplitDateTime
    )
    end_date = forms.SplitDateTimeField(
        label='End Date',
        help_text='Choose end date to populate test records to.',
        required=True,
        widget=AdminSplitDateTime
    )


class AlertAllocateResourceForm(forms.Form):
    pass
