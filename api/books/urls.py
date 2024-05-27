from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BooksViewSet, CommentViewSet, RatingViewSet, MyBooksViewSet

router = DefaultRouter(root_renderers="pretty_json")
router.register(r"my-books", MyBooksViewSet, basename="my-books")
router.register(r"(?P<book_id>[\w-]+)/comments", CommentViewSet, basename="comments")
router.register(r"(?P<book_id>[\w-]+)/review", RatingViewSet, basename="review")
router.register(r"", BooksViewSet, basename="books")

urlpatterns = [
    path("", include(router.urls), name="books"),
]
