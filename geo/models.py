from django.db import models
from jsonfield import JSONField
from .geocode import geocode, GeocodeResult


class Coordinate(models.Model):
    """
    Represents coordinates at geographic coordinate system
    """

    longitude = models.FloatField(blank=False)

    latitude = models.FloatField(blank=False)

    class Meta:
        abstract = True


class AddressManager(models.Manager):
    def create_with_location(self, location):
        """
        Given an arbitrary location string, attempt to *synchronously*
        perform a geocode and create an Address from the result.

        If the result is invalid, or geocoding fails, this will return None.
        Otherwise, it will return the newly created Address instance.

        If you want asynchronous behavior, you'll have to create it elsewhere.
        """
        result = geocode(location)
        return self.create_with_geocode_result(result)

    def create_with_geocode_result(self, result):
        """
        Given a GeocodeResult, validate it and return an Address.

        If the result is invalid, this will return None.
        """
        address = None
        if result and result.is_complete:
            address = self.create(
                street_address_1=result.street_address,
                street_address_2='',
                city=result.city,
                state=result.state,
                zip_code=result.zip5,
                country=result.country,
                geocode_json=result.geocode_json,
                latitude=result.latitude,
                longitude=result.longitude,
            )
        return address


class Address(Coordinate):
    """
    Represents an address with Google geocoding
    """

    objects = AddressManager()

    street_address_1 = models.CharField(
        null=True, blank=True, max_length=255, help_text='Street address 1'
    )

    street_address_2 = models.CharField(
        null=True, max_length=255, blank=True, default='', help_text='Street address 2'
    )

    city = models.CharField(blank=False, max_length=128)

    state = models.CharField(blank=False, help_text='State / Province', max_length=128)

    zip_code = models.CharField(null=True, blank=True, max_length=32, help_text='ZIP5')

    country = models.CharField(blank=False, max_length=128)

    geocode_json = JSONField(
        blank=True,
        null=True,
        default=None,
        help_text='Raw JSON response from google geocode',
    )

    @property
    def geocode_result(self):
        try:
            return GeocodeResult(self.geocode_json)
        except Exception:
            return None

    @property
    def formatted_address(self):
        return ', '.join(
            [comp for comp in [
                self.street_address_1,
                self.city,
                self.state,
            ] if comp]
        )

    def __str__(self):
        return self.formatted_address or str(self.id)
