# django-oscar-payu #

Following are the configurations required for setting up django-oscar-payu

### Installation ###

`pip install django-oscar-payu`

### Getting Started ###
Add the following to the `setting.py` file of your django-oscar setup

`PAYU_INFO = {
    'INR': {
        'merchant_key': "gtKFFx",
        'merchant_salt': "eCwWELxi",
        # for production environment use 'https://secure.payu.in/_payment'
        'payment_url': 'https://test.payu.in/_payment',
    }
}`


run `migrate.py` on  --> python manage.py migrate


Add following to the dashboard navigation

`
OSCAR_DASHBOARD_NAVIGATION.append({
    'label': _('Payments'),
    'icon': 'icon-globe',
    'children': [
        {
            'label': _('Paypal Express transactions'),
            'url_name': 'paypal-express-list',
        },
        {
            'label': _('Payu transactions'),
            'url_name': 'payu-nonseamless-list',
        },
        {
            'label': _('COD Transaction Lists'),
            'url_name': 'cashondelivery-transaction-list',
        },
    ]
})
`

