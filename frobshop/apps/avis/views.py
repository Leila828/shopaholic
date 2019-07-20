from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, View

from oscar.apps.catalogue.reviews.signals import review_added
from oscar.core.loading import get_classes, get_model
from oscar.core.utils import redirect_to_referrer
from .forms import *
from .models import *
from apps.service.models import *


class CreateServiceeReview(CreateView):
    model = ServiceReview
    form_class = ServiceReviewForm
    template_name = 'service/reviews/review_form.html'

    def form_valid(self, form):
        review = form.save(commit=False)
       # review.user = user.objects.get(pk=(self.request.user.pk))
        review.service = service.objects.get(pk=(self.request.service.pk))
        review.save()
        return reverse('service:detail')

class CreateServiceReview(CreateView):
    template_name = "service/reviews/review_form.html"
    model = ServiceReview
    product_model = service
    form_class = ServiceReviewForm
    view_signal = review_added

    def dispatch(self, request, *args, **kwargs):
        self.service = get_object_or_404(
            self.product_model, pk=kwargs.get("pk"))
        # check permission to leave review
        if not self.service.is_review_permitted(request.user):
            if self.service.has_review_by(request.user):
                message = _("You have already reviewed this service!")
            else:
                message = _("You can't leave a review for this service.")
            messages.warning(self.request, message)
            return redirect(self.service.get_absolute_url())

        return super().dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = self.service
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['service'] = self.service
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_signal(self.request, response, self.object)
        return response

    def get_success_url(self):
        messages.success(
            self.request, _("Thank you for reviewing this service"))
        return self.service.get_absolute_url()

    def send_signal(self, request, response, review):
        self.view_signal.send(sender=self, review=review, user=request.user,
                              request=request, response=response)


class ServiceReviewDetail(DetailView):
    template_name = "service/reviews/review_detail.html"
    context_object_name = 'review'
    model = ServiceReview
    product_model = service


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(
        self.product_model, pk=kwargs.get("pk"))
        return context


