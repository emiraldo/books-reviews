from django_celery_results.models import TaskResult
from factory.django import DjangoModelFactory
import factory

from .models import Reviewer, BookReview


class ReviewerFactory(DjangoModelFactory):

    class Meta:
        model = Reviewer


class BookReviewFactory(DjangoModelFactory):

    class Meta:
        model = BookReview


class TaskResultFactory(DjangoModelFactory):

    class Meta:
        model = TaskResult

    task_id = factory.Faker('uuid4')
    result = '[]'