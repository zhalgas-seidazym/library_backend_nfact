from django.contrib import admin

from .models import FriendRequest, Friend

admin.site.register(Friend)
admin.site.register(FriendRequest)
