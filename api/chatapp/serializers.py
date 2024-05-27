from rest_framework import serializers

from api.chatapp.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'sender', 'receiver', 'message', 'is_read', 'created_at']
        read_only_fields = ['user', 'sender']
