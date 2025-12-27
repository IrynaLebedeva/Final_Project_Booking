from rest_framework import serializers

from booking.models import Property
from booking.serializers.user import UserShortSerializer


class PropertyShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
        ]
        read_only_fields = ('id',)

class PropertySerializer(serializers.ModelSerializer):
    owner = UserShortSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
