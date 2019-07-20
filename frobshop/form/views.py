from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from oscar.core.loading import get_model
from oscar.apps.dashboard.partners.forms import PartnerAddressForm, PartnerCreateForm
from .forms import PartenaireAdressForm
from django.views import generic
from oscar.apps.catalogue.abstract_models import *
@login_required
def apply_for_partner(request):
    if request.method == 'POST':
        data = request.POST
        user = request.user
        country_model = get_model('address', 'Country')
        address_model = get_model('partner', 'PartenaireAdress')
        dashboard_perm = Permission.objects.get(
            codename='dashboard_access', content_type__app_label='partner')
        user.user_permissions.add(dashboard_perm)
        partner = PartnerCreateForm(data).save()
        country = country_model.objects.get(iso_3166_1_a2=data.get('country'))
        address = address_model(country = country, first_name=data.get('name'), line1=data.get('line1'), line2=data.get('line2'), line3=data.get('line3'), line4=data.get('line4'), partner=partner, postcode=data.get('postcode'), wilaya=data.get('wilaya'))
        address.save()
        partner.users.add(user)
        partner.save()
        return HttpResponseRedirect('/dashboard/')

    return render(request, 'form/form.html', {'PartnerCreateForm': PartnerCreateForm,'PartenaireAdressForm': PartenaireAdressForm})


