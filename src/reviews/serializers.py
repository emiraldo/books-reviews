import json

from django_celery_results.models import TaskResult
from rest_framework.fields import ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import BookReview


class TaskResultModelSerializer(ModelSerializer):

    results = SerializerMethodField()

    class Meta:
        model = TaskResult
        fields = ('status', 'date_created', 'date_done', 'results')

    def get_results(self, obj):
        return json.loads(obj.result)

class BookReviewModelSerializer(ModelSerializer):
    class Meta:
        model = BookReview
        fields = ('book_id', 'book_url', 'created', 'username', 'review')


class BookReviewCreateSerializer(Serializer):
    reviews = ListField()
