import uuid
from django.db import models
from api.users.models import User


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_friend_requests")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_friend_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name="unique_friend_requests")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_user} wants to be friends with {self.to_user}"


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_friends")
    friend_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_of_user_friends")
    created_at = models.DateTimeField(auto_now_add=True)
