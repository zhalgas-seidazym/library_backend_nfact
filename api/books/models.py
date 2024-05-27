import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.users.models import User


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=155, db_index=True, null=False, blank=False)
    cover = models.ImageField(upload_to='medias/book/covers/')
    description = models.TextField(null=False, blank=False)
    book = models.FileField(upload_to='medias/book/books/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    book_author = models.CharField(max_length=60, db_index=True, default="Unknown")
    is_private = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_user')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(null=False, blank=False, max_length=500)
    changed = models.BooleanField(default=False)
    commented_at = models.DateTimeField(auto_now_add=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments_book')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comments_user')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    child = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='ratings_user')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings_book')
