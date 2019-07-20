from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from treebeard.forms import movenodeform_factory
from apps.service.models import service as Service,ServiceImage
from apps.service.models import category as Category
from i18n.oscar.src.oscar.forms.widgets import ImageInput

CategoryForm = movenodeform_factory(
    Category,
    fields=['name', 'description', 'image'])

class CategoryFormCreate(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name','image','description'
        ]


class ServiceSearchForm(forms.Form):
    UPC = forms.CharField(max_length=255, required=False, label=_('UPC'))
    name = forms.CharField(
        max_length=255, required=False, label=_('Nom du service'))

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['name'] = cleaned_data['name'].strip()
        return cleaned_data


class ServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = [
            'category','UPC', 'name', 'description', 'tel', 'email', 'ville', 'wilaya']



class ServiceImageForm(forms.ModelForm):

    class Meta:
        model = ServiceImage
        fields = ['image', 'display_order']


class ServiceMultiForm(forms.ModelForm):
    form_classes = {
        'service': ServiceForm,
        'images': ServiceImageForm,
    }