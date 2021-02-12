import json
import uuid
from unittest import mock

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, \
    HTTP_200_OK
from rest_framework.test import APIClient

from reviews.exceptions import RecordPerMinute, GoogleApiError
from reviews.factories import ReviewerFactory, TaskResultFactory, \
    BookReviewFactory
from reviews.models import BookReview

class BookReviewModel(TestCase):

    def setUp(self):
        self.reviewer = ReviewerFactory()


    def test_create_per_minute(self):
        BookReviewFactory(
            username=self.reviewer.username,
            book_id='QnghAQAAIAAJ',
            review='test'
        )

        with self.assertRaises(RecordPerMinute):
            BookReviewFactory(
                username=self.reviewer.username,
                book_id='QnghAQAAIAAJ',
                review='test'
            )

    def test_get_book_url(self):
        book_url = BookReviewFactory(
            username=self.reviewer.username,
            book_id='QnghAQAAIAAJ',
            review='test'
        ).book_url

        self.assertEqual(book_url, 'https://www.googleapis.com/books/v1/volumes/QnghAQAAIAAJ')

    def test_get_book_url_error(self):
        with self.assertRaises(GoogleApiError):
            BookReviewFactory(
                username=self.reviewer.username,
                book_id='test',
                review='test'
            )


class BulkBookReviewCreate(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.reviwer = ReviewerFactory()

    @mock.patch(
        'reviews.views.book_review_create',
        return_value=TaskResultFactory()
    )
    def test_create_success(self, _):
        url = reverse('reviewers:bulk')
        payload = {
            "reviews": [
                {
                    'book_id': 'QnghAQAAIAAJ',
                    'user_id': str(self.reviwer.id),
                    'review': 'test'
                }
            ]
        }

        payload = json.dumps(payload)

        response  = self.client.post(
            url, data=payload, content_type='application/json'
        )

        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)

    def test_create_error(self):
        url = reverse('reviewers:bulk')
        payload = {}

        payload = json.dumps(payload)

        response  = self.client.post(
            url, data=payload, content_type='application/json'
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class TrackingBookReview(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.reviwer = ReviewerFactory()

    def test_get_tracking(self,):
        task = TaskResultFactory()

        response = self.client.get(
            reverse(
                'reviewers:tracking',
                kwargs={
                    "task_id": task.task_id
                }
            ), content_type='application/json'
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
