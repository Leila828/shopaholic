from __future__ import unicode_literals

import json
import logging

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.views.generic import RedirectView, FormView
from oscar.core.exceptions import ModuleNotFoundError
from oscar.core.loading import get_class, get_model

from payu.exceptions import PayuError
from payu.nonseamless.exceptions import EmptyBasketException, InvalidBasket, MissingShippingAddressException, \
    MissingShippingMethodException
from payu.nonseamless.facade import set_txn, generate_hash, verify_hash, PAYU_INFO

# Load views dynamically
from payu.nonseamless.forms import PayUForm
from payu.nonseamless.models import NonSeamlessTransaction

PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')

ShippingAddress = get_model('order', 'ShippingAddress')
Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
Repository = get_class('shipping.repository', 'Repository')
Selector = get_class('partner.strategy', 'Selector')
Source = get_model('payment', 'Source')
SourceType = get_model('payment', 'SourceType')
try:
    Applicator = get_class('offer.applicator', 'Applicator')
except ModuleNotFoundError:
    # fallback for django-oscar<=1.1
    Applicator = get_class('offer.utils', 'Applicator')

logger = logging.getLogger('payu.nonseamless')


class RedirectView(CheckoutSessionMixin, RedirectView):
    """
    Initiate the transaction with Paypal and redirect the user
    to PayPal's Express Checkout to perform the transaction.
    """
    permanent = False

    # Setting to distinguish if the site has already collected a shipping
    # address.  This is False when redirecting to PayPal straight from the
    # basket page but True when redirecting from checkout.
    as_payment_method = False

    def get_redirect_url(self, **kwargs):
        try:
            basket = self.build_submission()['basket']
            supported_currency = settings.PAYU_INFO.keys()
            if basket.currency not in supported_currency:
                messages.error(self.request, "Unsupported Currency")
                return reverse('basket:summary')
            else:
                url = self._get_redirect_url(basket, **kwargs)
        except PayuError as ppe:
            messages.error(self.request, ppe.message)
            if self.as_payment_method:
                url = reverse('checkout:payment-details')
            else:
                url = reverse('basket:summary')
            return url
        except InvalidBasket as e:
            messages.warning(self.request, six.text_type(e))
            return reverse('basket:summary')
        except EmptyBasketException:
            messages.error(self.request, _("Your basket is empty"))
            return reverse('basket:summary')
        except MissingShippingAddressException:
            messages.error(
                    self.request, _("A shipping address must be specified"))
            return reverse('checkout:shipping-address')
        except MissingShippingMethodException:
            messages.error(
                    self.request, _("A shipping method must be specified"))
            return reverse('checkout:shipping-method')
        else:
            basket.freeze()
            logger.info("Basket #%s - redirecting to %s", basket.id, url)
            return url

    def _get_redirect_url(self, basket, **kwargs):
        if basket.is_empty:
            raise EmptyBasketException()

        # redirect to forms page where form would submit through webpage to payu
        # record the transaction
        shipping_addr = self.get_shipping_address(basket)
        order_total = self.build_submission()['order_total']
        if self.request.user.is_authenticated():
            email = self.request.user.email
        else:
            email = self.build_submission()['order_kwargs']['guest_email']
        txn = set_txn(basket, basket.currency, email, order_total, user_address=shipping_addr)

        return reverse('payu-pre-redirect', kwargs={'txn_id': txn.txnid})

    def _get_payu_params(self):
        """
        Return any additional PayPal parameters
        """
        PAYU_INFO = {
            'merchant_key': "C0Dr8m",
            'merchant_salt': "3sf0jURk",
            # for production environment use 'https://secure.payu.in/_payment'
            'payment_url': 'https://test.payu.in/_payment',
        }
        return getattr(settings, 'PAYU_INFO', PAYU_INFO)


class PayuPreRquestView(FormView):
    template_name = 'payu/nonseamless/payu_form.html'
    form_class = PayUForm

    def get(self, request, *args, **kwargs):
        self.txn = get_object_or_404(NonSeamlessTransaction, txnid=kwargs['txn_id'])
        return super(PayuPreRquestView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        conetxt = super(PayuPreRquestView, self).get_context_data(**kwargs)
        conetxt['action'] = settings.PAYU_INFO.get(self.request.session['currency']).get('payment_url')

        return conetxt

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        salt = settings.PAYU_INFO.get(self.request.session['currency']).get('merchant_salt')
        key = settings.PAYU_INFO.get(self.request.session['currency']).get('merchant_key')
        txn = self.txn
        curl = self.request.build_absolute_uri(reverse('payu-fail-response', kwargs={'txn_id': txn.txnid}))
        furl = self.request.build_absolute_uri(reverse('payu-cancel-response', kwargs={'txn_id': txn.txnid}))
        surl = self.request.build_absolute_uri(reverse('payu-place-order', kwargs={'txn_id': txn.txnid}))

        # print self.txn_id
        initial = super(PayuPreRquestView, self).get_initial()

        initial['key'] = key
        initial['txnid'] = txn.txnid
        initial['productinfo'] = txn.productinfo.encode('ascii', 'ignore').strip()
        initial['amount'] = txn.amount
        initial['firstname'] = txn.firstname
        initial['lastname'] = txn.lastname
        initial['email'] = txn.email
        initial['phone'] = txn.phone
        initial['phone'] = txn.phone
        initial['address1'] = txn.address1
        initial['address2'] = txn.address2
        initial['city'] = txn.city
        initial['state'] = txn.state
        initial['country'] = txn.country
        initial['zipcode'] = txn.zipcode
        initial['hash'] = generate_hash(initial, salt)
        initial['surl'] = surl
        initial['furl'] = furl
        initial['curl'] = curl

        return initial


class CancelResponseView(RedirectView):
    permanent = False
    cancelled = False

    def get(self, request, *args, **kwargs):
        txn = get_object_or_404(NonSeamlessTransaction, txnid=kwargs['txn_id'])

        if self.cancelled:
            txn.response = 'C'
        else:
            txn.response = 'F'

        txn.raw_response = json.dumps(self.request.POST)
        txn.save()
        basket = get_object_or_404(Basket, id=txn.basket, status=Basket.FROZEN)
        basket.thaw()
        logger.info("Payment cancelled (token %s) - basket #%s thawed", request.GET.get('token', '<no token>'),
                    basket.id)
        return super(CancelResponseView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        txn = get_object_or_404(NonSeamlessTransaction, txnid=kwargs['txn_id'])

        if self.cancelled:
            txn.response = 'C'
        else:
            txn.response = 'F'

        txn.raw_response = json.dumps(self.request.POST)
        txn.save()
        basket = get_object_or_404(Basket, id=txn.basket, status=Basket.FROZEN)
        basket.thaw()
        logger.info("Payment cancelled (token %s) - basket #%s thawed", request.GET.get('token', '<no token>'),
                    basket.id)
        return super(CancelResponseView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, _("Payu transaction cancelled"))
        return reverse('basket:summary')


class SuccessResponseView(PaymentDetailsView):
    template_name_preview = 'payu/nonseamless/preview.html'
    preview = True
    txn = None

    @property
    def pre_conditions(self):
        return []

    def load_frozen_basket(self, basket_id):
        # Lookup the frozen basket that this txn corresponds to
        try:
            basket = Basket.objects.get(id=basket_id, status=Basket.FROZEN)
        except Basket.DoesNotExist:
            return None

        # Assign strategy to basket instance
        if Selector:
            basket.strategy = Selector().strategy(self.request)

        # Re-apply any offers
        # Applicator().apply(request=self.request, basket=basket)
        Applicator().apply(basket, self.request.user, self.request)

        print basket.offer_applications.offers

        return basket

    def get_context_data(self, **kwargs):
        ctx = super(SuccessResponseView, self).get_context_data(**kwargs)

        return ctx

    def post(self, request, *args, **kwargs):
        """
        Place an order.

        We fetch the txn details again and then proceed with oscar's standard
        payment details view for placing the order.
        """

        error_msg = _(
                "A problem occurred communicating with Payu "
                "- please try again later"
        )

        self.txn = get_object_or_404(NonSeamlessTransaction, txnid=kwargs['txn_id'])
        self.txn.response = 'S'

        self.txn.raw_response = json.dumps(self.request.POST)
        self.txn.save()
        salt = settings.PAYU_INFO.get(self.request.session['currency']).get('merchant_salt')
        if not verify_hash(request.POST, salt):
            messages.error(self.request, error_msg)
            return HttpResponseRedirect(reverse('basket:summary'))

        basket = self.load_frozen_basket(self.txn.basket)
        if not basket:
            messages.error(self.request, error_msg)
            return HttpResponseRedirect(reverse('basket:summary'))

        submission = self.build_submission(basket=basket)
        return self.submit(**submission)

    def build_submission(self, **kwargs):
        submission = super(SuccessResponseView, self).build_submission(**kwargs)
        submission['payment_kwargs']['txn'] = self.txn
        return submission

    def handle_payment(self, order_number, total, **kwargs):
        """
        Complete payment with PayPal - this calls the 'DoExpressCheckout'
        method to capture the money from the initial transaction.
        """
        kwargs['txn'].orderid = order_number
        kwargs['txn'].save()

        # Record payment source and event
        source_type, is_created = SourceType.objects.get_or_create(
                name='Payu')
        source = Source(source_type=source_type,
                        currency=kwargs['txn'].currency,
                        amount_allocated=kwargs['txn'].amount,
                        amount_debited=kwargs['txn'].amount,
                        reference=kwargs['txn'].txnid)

        self.add_payment_source(source)
        self.add_payment_event('Settled', kwargs['txn'].amount, reference=kwargs['txn'].txnid)
