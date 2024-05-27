from rest_framework import serializers
from .models import FriendRequest, Friend


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
        read_only_fields = ['from_user', 'accepted']


class FriendSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    def get_user(self):
        return self.context['request'].user

    def get_friends(self):
        friends = Friend.objects.filter(user=self.context['request'].user).all()
        return friends
