from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FriendRequestViewSet,
    friend_requests,
    my_requests,
    request_action,
    get_friends,
    delete_friend,
)

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('', include(router.urls)),
    path('friend-requests/', friend_requests, name='friend-requests'),
    path('my-requests/', my_requests, name='my-requests'),
    path('request-action/<int:pk>/', request_action, name='request-action'),
    path('get-friends/', get_friends, name='get-friends'),
    path('delete-friend/<int:pk>/', delete_friend, name='delete-friend'),
]
