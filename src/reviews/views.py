import json

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_celery_results.models import TaskResult
from django_filters.rest_framework import FilterSet, CharFilter, \
    DateFromToRangeFilter, DateFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import BookReview, Reviewer
from .serializers import BookReviewCreateSerializer, TaskResultModelSerializer, \
    BookReviewModelSerializer
from .tasks import book_review_create


class BulkBookReviewCreate(APIView):

    @swagger_auto_schema(
        responses={
            202: '{"msg": "accepted", "tracking_url": ""}',
            400: '{"msg": "bad request"}'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reviews': openapi.Schema(
                    type=openapi.TYPE_ARRAY, description='Array of reviews',
                    items=openapi.Items(type=openapi.TYPE_OBJECT)
                )
            }
        )
    )
    def post(self, request):
        data = BookReviewCreateSerializer(data=request.data)
        if data.is_valid():
            task = book_review_create.delay(data.data.get('reviews'))
            return Response(
                status=HTTP_202_ACCEPTED,
                data={
                    "msg": "accepted",
                    "tracking_url": reverse(
                        'reviewers:tracking',
                        kwargs={
                            "task_id": task.task_id
                        }
                    )
                }
            )
        else:
            return Response(status=HTTP_400_BAD_REQUEST, data={})

class TrackingBookReviewCreate(APIView):

    @swagger_auto_schema(
        responses={
            200: TaskResultModelSerializer(),
        }
    )
    def get(self, request, task_id):
        task_result = get_object_or_404(TaskResult, task_id=task_id)
        return Response(TaskResultModelSerializer(task_result).data)


class BookReviewFilter(FilterSet):
    user_id = CharFilter(method='filter_by_user')
    book_id = CharFilter(field_name='book_id')
    start_date = DateFilter(field_name='created', lookup_expr="gte")
    end_date = DateFilter(field_name='created', lookup_expr="lte")
    date = DateFilter(field_name='created', lookup_expr='contains')

    def filter_by_user(self, queryset, name, value):
        user = get_object_or_404(Reviewer, pk=value)
        return queryset.filter(username=user.username)

    class Meta:
        model = BookReview
        fields = ['book_id',]


class BookReviewList(ListAPIView):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewModelSerializer
    filterset_class = BookReviewFilter
