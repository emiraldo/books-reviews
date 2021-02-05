from django.contrib import admin

from .models import Reviewer, BookReview

@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = list_display
    readonly_fields = ('id', )

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_url', 'username', 'created')
    list_display_links = list_display
    readonly_fields = (
        'id',
        'book_id',
        'book_url',
        'created',
        'username',
        'review'
    )
