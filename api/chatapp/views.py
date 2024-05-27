from django.db.models import Subquery, OuterRef, Q
from rest_framework import generics

from api.chatapp.models import Message
from api.chatapp.serializers import MessageSerializer
from api.users.models import User


class MyChatsView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
