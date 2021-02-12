from django.urls import path

from .views import BulkBookReviewCreate, TrackingBookReviewCreate

app_name = 'book-review'

urlpatterns = [
    path("book-review/bulk/", BulkBookReviewCreate.as_view(), name='bulk'),
    path("book-review/tracking/<str:task_id>",
         TrackingBookReviewCreate.as_view(), name='tracking')
]