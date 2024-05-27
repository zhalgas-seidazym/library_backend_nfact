from django.db.models import Q
from django.db import transaction

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from ..users.models import User
from .models import Friend, FriendRequest
from ..books.permissions import IsOwnerOrReadOnly
from .serializers import FriendRequestSerializer, FriendSerializer


class FriendRequestViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def perform_create(self, serializer):
        to_user_id = self.request.data.get('to_user')
        try:
            to_user_model = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request_to_current_user = FriendRequest.objects.filter(
            Q(from_user=to_user_model) & Q(to_user=self.request.user)
        ).first()

        my_request = FriendRequest.objects.filter(
            Q(from_user=self.request.user) & Q(to_user=to_user_model)
        ).first()

        if friend_request_to_current_user:
            if friend_request_to_current_user.accepted:
                return Response({'message': 'Friend request already accepted'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        if my_request:
            return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(from_user=self.request.user, to_user=to_user_model)
        return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests(request, *args, **kwargs):
    requests_queryset = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    serializer = FriendRequestSerializer(requests_queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_requests(request, *args, **kwargs):
    requests_queryset = FriendRequest.objects.filter(from_user=request.user, accepted=False)
    serializer = FriendRequestSerializer(requests_queryset, many=True)
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def request_action(request, *args, **kwargs):
    try:
        request_id = FriendRequest.objects.get(pk=kwargs['pk'], to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({"message": "Friend request does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        action_type = request.query_params.get('action')
        if action_type == 'accept':
            friend_user = request_id.from_user
            request_id.accepted = True
            request_id.save()
            Friend.objects.create(user=request.user, friend=friend_user)
            return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        request_id.delete()
        return Response({'message': 'Friend request declined'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(request, *args, **kwargs):
    queryset = Friend.objects.filter(user=request.user).all()
    serializer = FriendSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def delete_friend(request, *args, **kwargs):
    try:
        friend = Friend.objects.get(pk=kwargs['pk'])
        friend.delete()
        return Response(status=status.HTTP_200_OK)
    except Friend.DoesNotExist:
        return Response("Not friend such id", status=status.HTTP_404_NOT_FOUND)
