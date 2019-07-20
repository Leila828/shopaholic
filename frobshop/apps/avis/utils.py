from django.conf import settings

from oscar.core.loading import get_model
from .models import *

def get_default_review_status():


    if settings.OSCAR_MODERATE_REVIEWS:
        return ServiceReview.FOR_MODERATION

    return ServiceReview.APPROVED
