from django.contrib import admin

from oscar.core.loading import get_model
from .models import *


class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'score', 'status', 'total_votes',
                    'delta_votes', 'date_created')
    readonly_fields = ('total_votes', 'delta_votes')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'delta', 'date_created')


admin.site.register(ServiceReview, ServiceReviewAdmin)
admin.site.register(Vote, VoteAdmin)
