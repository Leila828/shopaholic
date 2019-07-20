from django.conf import settings

from oscar.core.loading import get_model


def get_default_review_status():
    ServiceReview = get_model('reviews', 'ServiceReview')

    if settings.OSCAR_MODERATE_REVIEWS:
        return ServiceReview.FOR_MODERATION

    return ServiceReview.APPROVED
