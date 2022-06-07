from rest_framework import serializers
from supermarket import models

class BasicItemInformationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'itemName',
            'id',
            'description',
            'categoryName',
            'unit',
            'entry_date'
        )
        model = models.Item

class ItemInstanceSerialzer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'instanceName',
            'instanceId',
            'status',
            'production_date',
            'expiry_date',
            'quantity',
            'entry_date',
        )
        model = models.ItemInstance