from rest_framework.fields import ListField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import BookReview


class BookReviewModelSerializer(ModelSerializer):
    class Meta:
        model = BookReview
        fields = ('book_id', 'book_url', 'created', 'username', 'review')


class BookReviewCreateSerializer(Serializer):
    reviews = ListField()
