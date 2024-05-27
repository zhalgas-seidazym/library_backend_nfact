from django.db.models import Count, Sum
from rest_framework import serializers
from .models import Book, Comment, Rating


class CommentChildSerializer(serializers.ModelSerializer):
    whom = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.email', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), source='parent.id', required=False,
                                                write_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'whom', 'parent', 'content', 'user', 'commented_at')

    def create(self, validated_data):
        if validated_data.get("parent"):
            parent_id = validated_data.pop('parent').get('id')
            parent_comment = Comment.objects.get(pk=parent_id.id)

            has_parent = parent_comment.parent
            if has_parent:
                return Comment.objects.create(child=parent_comment, parent=has_parent, **validated_data)
            else:
                validated_data['parent'] = parent_comment
                return Comment.objects.create(child=parent_comment, **validated_data)
        return Comment.objects.create(**validated_data)

    def get_whom(self, obj):
        if obj.child is None:
            return None
        return obj.child.user.email


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)
    content = serializers.CharField()
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'reply_count', 'changed', 'commented_at', 'content', 'replies']
        extra_kwargs = {
            "user": {"read_only": True},
            "book": {"read_only": True},
            "changed": {"read_only": True},
            "commented_at": {"read_only": True},
        }

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.changed = True
        instance.save()
        return instance

    def get_reply_count(self, obj):
        return obj.children().count()

    def get_replies(self, obj):
        return CommentChildSerializer(obj.children(), many=True).data


class BookViewSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'book_author', 'rating', 'view_count', 'is_private']
        read_only_fields = ['view_count']

    def get_rating(self, obj):
        ratings = Rating.objects.filter(book=obj).aggregate(
            total_rating=Sum('rating'),
            rating_count=Count('rating')
        )

        if ratings['rating_count']:
            avg_rating = ratings['total_rating'] / ratings['rating_count']
        else:
            avg_rating = 0

        return avg_rating




class BookSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title',
                  'cover', 'description',
                  'book',
                  'rating', 'uploaded_at',
                  'is_private',
                  'book_author', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return Book.objects.create(user=user, **validated_data)

    def get_rating(self, obj):
        ratings = Rating.objects.filter(book=obj).aggregate(
            total_rating=Sum('rating'),
            rating_count=Count('rating')
        )

        if ratings['rating_count']:
            avg_rating = ratings['total_rating'] / ratings['rating_count']
        else:
            avg_rating = 0

        return {
            'total': avg_rating,
            5: Rating.objects.filter(book=obj, rating=5).count(),
            4: Rating.objects.filter(book=obj, rating=4).count(),
            3: Rating.objects.filter(book=obj, rating=3).count(),
            2: Rating.objects.filter(book=obj, rating=2).count(),
            1: Rating.objects.filter(book=obj, rating=1).count(),
        }


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user', 'book']
