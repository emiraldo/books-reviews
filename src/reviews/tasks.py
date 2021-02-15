from celery import shared_task

from .exceptions import RecordPerMinute, GoogleApiError
from .models import BookReview, Reviewer
from .serializers import BookReviewModelSerializer


@shared_task()
def book_review_create(data):
    results = []
    for review in data:
        try:
            user = Reviewer.objects.get(
                id=review.get('user_id')
            )
            book_review = BookReview.objects.create(
                book_id=review.get('book_id'),
                username=user.username,
                review=review.get('review')
            )

            results.append(
                BookReviewModelSerializer(book_review).data
            )
        except Reviewer.DoesNotExist as e:
            results.append({
                'book_id': review.get('book_id'),
                'error': e.__str__()
            }
            )
        except RecordPerMinute as e:
            results.append({
                'book_id': review.get('book_id'),
                'error': e.__str__()
            }
            )
        except GoogleApiError as e:
            results.append({
                'book_id': review.get('book_id'),
                'error': e.__str__()
            }
            )
        except Exception as e:
            results.append({
                'book_id': review.get('book_id'),
                'error': e.__str__()
            }
            )

    return results
