from rest_framework import serializers

from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    '''Serializes user notification record.'''
    type = serializers.StringRelatedField()

    class Meta:
        model = Notification

        fields = [
            'id', 'type',
            'message', 'is_read', 'is_active', 'created_at'
        ]

        extra_kwargs = {
            'type': {'read_only': True},
            'message': {'read_only': True},
            'created_at': {'read_only': True},
            'is_active': {'read_only': True},
            'is_read': {'read_only': True},
        }
