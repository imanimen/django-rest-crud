# serialize data to return models
from rest_framework import serializers
from base.models import Item

class ItemSerializer(serializers.ModelSerializer):
    # created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Item
        # fields = ('name', 'id')
        fields = '__all__'
    