from django import forms
from django.templatetags.static import static


class TempReportImportForm(forms.Form):
    json = forms.FileField(
        label='JSON File',
        help_text='Choose a json file that contains reports data from legacy web app. <a href="{}" download>Click Here</a> to download a sample JSON file.'.format(static('sample_downloads/WQReports.json')),
        required=True,
    )
