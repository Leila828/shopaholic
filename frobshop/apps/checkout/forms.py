from oscar.apps.checkout.forms import ShippingAddressForm


class Formulaire(ShippingAddressForm):
    class Meta:
        fields = [
            'title', 'first_name', 'last_name',
            'line1', 'line2', 'line3', 'line4',
            'state', 'postcode', 'country',
            'phone_number', 'notes', 'wilaya',
        ]