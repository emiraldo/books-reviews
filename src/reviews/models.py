import uuid

import requests
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .exceptions import RecordPerMinute, GoogleApiError


class Reviewer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class BookReview(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book_id = models.CharField(max_length=255)
    book_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)
    review = models.TextField()

    def __str__(self):
        return f"Review - {self.book_id} - {self.username}"

    def _get_book_url(self):
        book_url = ''
        base_url = settings.GOOGLEAPI_BOOKS
        response = requests.get(f"{base_url}{self.book_id}")
        if response.status_code == 200:
            json_response = response.json()
            book_url = json_response.get('selfLink', None)
        else:
            raise GoogleApiError
        return book_url


@receiver(pre_save, sender=BookReview, weak=False)
def book_review_validation(sender, instance, *args, **kwargs):
    instance.book_url = instance._get_book_url()
    if instance._state.adding:
        try:
            last_review = BookReview.objects.filter(
                username=instance.username,
                book_id=instance.book_id
            ).latest('created')
            if last_review:
                now = timezone.now()
                last_created = last_review.created + \
                               timezone.timedelta(minutes=1)
                if now < last_created:
                    raise RecordPerMinute
        except BookReview.DoesNotExist:
            pass
