from rest_framework import serializers

from geo.models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'street_address_1',
            'street_address_2',
            'city',
            'state',
            'zip_code',
            'country',
            'longitude',
            'latitude',
            'formatted_address',
        )
