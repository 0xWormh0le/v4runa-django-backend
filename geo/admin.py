from django.contrib import admin

from common.admin import admin_site
from .forms import LocationForm, AddressForm
from .models import Address


@admin.register(Address, site=admin_site)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('formatted_address', 'zip_code')
    list_filter = ('state',)
    search_fields = (
        'street_address_1',
        'street_address_2',
        'city',
        'state',
        'zip_code',
        'country'
    )

    ADDRESS_FIELDS = [
        'street_address_1',
        'street_address_2',
        'city',
        'state',
        'zip_code',
        'country',
        'geocode_json',
        'latitude',
        'longitude',
    ]

    LOCATION_FIELD = ['location']

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = LocationForm if obj is None else AddressForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        return self.LOCATION_FIELD if obj is None else self.ADDRESS_FIELDS

    # def get_readonly_fields(self, request, obj=None):
    #     return [] if obj is None else self.ADDRESS_FIELDS
