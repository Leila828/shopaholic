from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from oscar.apps.catalogue.reviews.utils import get_default_review_status
from oscar.core import validators
from oscar.core.compat import AUTH_USER_MODEL
from oscar.core.loading import get_class
from apps.service.models import *

from .managers import *

class ServiceReview(models.Model):

    service = models.ForeignKey(
        service, related_name='avis', null=True,
        on_delete=models.CASCADE)

    # Scores are between 0 and 5
    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])
    score = models.SmallIntegerField(_("Score"), choices=SCORE_CHOICES)

    title = models.CharField(
        verbose_name=pgettext_lazy("Service review title", "Title"),
        max_length=255, validators=[validators.non_whitespace])

    body = models.TextField(_("Body"))

    # User information.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='avis')

    # Fields to be completed if user is anonymous
    name = models.CharField(
        pgettext_lazy("Anonymous reviewer name", "Name"),
        max_length=255, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    homepage = models.URLField(_("URL"), blank=True)

    FOR_MODERATION, APPROVED, REJECTED = 0, 1, 2
    STATUS_CHOICES = (
        (FOR_MODERATION, _("Requires moderation")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )

    status = models.SmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=get_default_review_status)

    # Denormalised vote totals
    total_votes = models.IntegerField(
        _("Total Votes"), default=0)  # upvotes + down votes
    delta_votes = models.IntegerField(
        _("Delta Votes"), default=0, db_index=True)  # upvotes - down votes

    date_created = models.DateTimeField(auto_now_add=True)

    # Managers
    objects = ServiceReviewQuerySet.as_manager()

    class Meta:
        app_label = 'avis'
        ordering = ['-delta_votes', 'id']

    def get_absolute_url(self):
        return reverse('catalogue:reviews-detail')

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.strip()
        self.body = self.body.strip()
        if not self.user and not (self.name and self.email):
            raise ValidationError(
                _("Anonymous reviews must include a name and an email"))

    def vote_up(self, user):
        self.vote.create(user=user, delta=Vote.UP)

    def vote_down(self, user):
        self.vote.create(user=user, delta=Vote.DOWN)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.service.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.service is not None:
            self.service.update_rating()

    # Properties

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def pending_moderation(self):
        return self.status == self.FOR_MODERATION

    @property
    def is_approved(self):
        return self.status == self.APPROVED

    @property
    def is_rejected(self):
        return self.status == self.REJECTED

    @property
    def has_votes(self):
        return self.total_votes > 0

    @property
    def num_up_votes(self):
        return int((self.total_votes + self.delta_votes) / 2)

    @property
    def num_down_votes(self):
        return int((self.total_votes - self.delta_votes) / 2)

    @property
    def reviewer_name(self):
        if self.user:
            name = self.user.name
            return name if name else _('anonymous')
        else:
            return self.name

    # Helpers

    def update_totals(self):
        """
        Update total and delta votes
        """
        result = self.vote.aggregate(
            score=Sum('delta'), total_votes=Count('id'))
        self.total_votes = result['total_votes'] or 0
        self.delta_votes = result['score'] or 0
        self.save()

    def can_user_vote(self, user):
        if not user.is_authenticated:
            return False, _("Only signed in users can vote")
        vote = self.vote.model(review=self, user=user, delta=1)
        try:
            vote.full_clean()
        except ValidationError as e:
            return False, "%s" % e
        return True, ""


class Vote(models.Model):
    review = models.ForeignKey(
        ServiceReview,
        on_delete=models.CASCADE,
        related_name='vote')
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='review_vote',
        on_delete=models.CASCADE)
    UP, DOWN = 1, -1
    VOTE_CHOICES = (
        (UP, _("Up")),
        (DOWN, _("Down"))
    )
    delta = models.SmallIntegerField(_('Delta'), choices=VOTE_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'avis'
        ordering = ['-date_created']

    def __str__(self):
        return "%s vote for %s" % (self.delta, self.review)

    def clean(self):
        if not self.review.is_anonymous and self.review.user == self.user:
            raise ValidationError(_(
                "You cannot vote on your own reviews"))
        if not self.user.primary_key:
            raise ValidationError(_(
                "Only signed-in users can vote on reviews"))
        previous_votes = self.review.vote.filter(user=self.user)
        if len(previous_votes) > 0:
            raise ValidationError(_(
                "You can only vote once on a review"))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.review.update_totals()

