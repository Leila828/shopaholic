from django.conf.urls import url
from form.views import *
from django.urls import path
from django.views.generic import TemplateView
app_name='form'

urlpatterns=[
    path('boutique/', apply_for_partner, name='index'),
    url(r'', TemplateView.as_view(template_name='form/descriptionBoutique.html'), name="description"),

]