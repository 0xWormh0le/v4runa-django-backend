from rest_framework import serializers

from utility.models import (
    AssetFinance,
    WaterQuality,
    WaterUtility,
)
from ..geo.serializers import AddressSerializer


class WaterUtilitySerializer(serializers.ModelSerializer):
    location = AddressSerializer()

    class Meta:
        model = WaterUtility
        fields = '__all__'


class WaterUtilityAutoCompleteSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, water_utility):
        return str(water_utility)

    class Meta:
        model = WaterUtility
        fields = (
            'id',
            'name',
        )


class AssetFinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetFinance
        fields = (
            'id',
            'water_utility',
            'asset_name',
            'projected_unscheduled_amount',
            'projected_scheduled_amount',
            'allocated_budget',
            'average_service_life',
        )


class WaterQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterQuality
        fields = '__all__'
