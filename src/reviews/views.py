import json

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_celery_results.models import TaskResult
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import BookReviewCreateSerializer
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
            print(task)
            print(task.task_id)
            return Response(
                status=HTTP_202_ACCEPTED,
                data={
                    "msg": "accepted",
                    "tracking_url": reverse(
                        'reviewers:tracking', kwargs={
                            "task_id": task.task_id
                        }
                    )
                }
            )
        else:
            return Response(status=HTTP_400_BAD_REQUEST, data={})

class TrackingBookReviewCreate(APIView):

    def get(self, request, task_id):
        task_result = get_object_or_404(TaskResult, task_id=task_id)
        return Response(
            {
                "status": task_result.status,
                "date_created": task_result.date_created,
                "date_done": task_result.date_done,
                "results": json.loads(task_result.result)
            }
        )