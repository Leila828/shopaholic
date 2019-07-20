from __future__ import unicode_literals

from hashlib import sha512
from uuid import uuid4

from django.conf import settings
from models import NonSeamlessTransaction

KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
        'udf9', 'udf10')

PAYU_INFO = {
    'INR': {
        'merchant_key': "gtKFFx",
        'merchant_salt': "eCwWELxi",
        # for production environment use 'https://secure.payu.in/_payment'
        'payment_url': 'https://test.payu.in/_payment',
    }
}


def generate_hash(data, salt):
    """
    Generates sha512 of form fields in following format.
    sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)
    sha512(key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||SALT)
    """
    hash_sum = sha512('')
    for key in KEYS:
        if key == 'productinfo':
            hash_sum.update("%s%s" % (data.get(key, '').encode('ascii', 'ignore').strip(), '|'))
        else:
            hash_sum.update("%s%s" % (str(data.get(key, '')), '|'))
    hash_sum.update(salt)
    return hash_sum.hexdigest().lower()


def verify_hash(data, salt):
    """
    Generates sha512 of received data fields in following format.
    sha512(SALT|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key)
    """
    KEYS_REVERSED = KEYS[::-1]
    hash_sum = sha512('')
    hash_sum.update(salt)
    hash_sum.update("%s%s" % ('|', str(data.get('status', ''))))
    for key in KEYS_REVERSED:
        hash_sum.update("%s%s" % ('|', str(data.get(key, ''))))
    return hash_sum.hexdigest().lower() == str(data.get('hash', ''))


def get_payu_url():
    """
    Return the URL for a PayPal Express transaction.

    This involves registering the txn with PayPal to get a one-time
    URL.  If a shipping method and shipping address are passed, then these are
    given to PayPal directly - this is used within when using PayPal as a
    payment method.
    """
    if getattr(settings, 'PAYU_TEST_MODE', True):
        return 'https://test.payu.in/_payment'
    else:
        return 'https://secure.payu.in/_payment'


def set_txn(basket, currency, email,  order_total, user_address=None):

    txn = NonSeamlessTransaction()
    txn.txnid = uuid4().hex[:28]
    txn.productinfo = basket.all_lines()[0].product.get_title()
    txn.amount = order_total.excl_tax
    txn.currency = currency
    txn.firstname = user_address.first_name
    txn.lastname = user_address.last_name
    txn.email = email
    txn.phone = user_address.phone_number.national_number if user_address.phone_number else 9999999999
    txn.address1 = user_address.line1[:46]
    txn.address2 = user_address.line2[:46]
    txn.city = user_address.line4
    txn.state = user_address.state
    txn.country = user_address.country
    txn.zipcode = user_address.postcode
    txn.response = 'N'
    txn.basket = basket.id
    txn.save()
    return txn
