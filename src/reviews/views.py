import json

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_celery_results.models import TaskResult
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import BookReviewCreateSerializer, TaskResultModelSerializer
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