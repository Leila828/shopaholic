from oscar.apps.dashboard.partners.forms import PartnerAddressForm
from .models import PartenaireAdress


class PartenaireAdressForm(PartnerAddressForm):
    class Meta:
        fields = ('name', 'line1', 'line2', 'line3', 'line4',
                  'wilaya', 'postcode', 'country')
        model = PartenaireAdress