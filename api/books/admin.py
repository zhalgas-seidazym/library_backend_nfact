from django.contrib import admin

from api.books.models import Book, Comment, Rating

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Rating)
