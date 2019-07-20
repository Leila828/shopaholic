from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from payu.nonseamless import views


urlpatterns = patterns(
    # Views for normal flow that starts on the basket page

    url(r'^preview/(?P<basket_id>\d+)/$',
        views.SuccessResponseView.as_view(preview=True),
        name='payu-success-response'),

    # View for using PayPal as a payment method
    url(r'^payment/', views.RedirectView.as_view(as_payment_method=True), name='payu-direct-payment'),


    # payu url ready to redirect to payu
    url(r'^redirect/', views.RedirectView.as_view(), name='payu-redirect'),
    url(r'^prepayment/(?P<txn_id>\w+)', views.PayuPreRquestView.as_view(), name='payu-pre-redirect'),
    url(r'^cancel/(?P<txn_id>\w+)/$', csrf_exempt(views.CancelResponseView.as_view(cancelled=True)), name='payu-cancel-response'),
    url(r'^cancel/(?P<txn_id>\w+)/$', csrf_exempt(views.CancelResponseView.as_view()), name='payu-fail-response'),
    url(r'^place-order/(?P<txn_id>\w+)/$', csrf_exempt(views.SuccessResponseView.as_view()), name='payu-place-order'),
)
