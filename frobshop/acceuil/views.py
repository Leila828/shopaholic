from django.db.transaction import commit
from django.views import generic
from oscar.apps.catalogue.models import *
from apps.service.filters import ServiceFilters
from apps.service.models import service

from django.shortcuts import render



from django.views import generic



from django.shortcuts import render, HttpResponseRedirect

class Index(generic.ListView):
    template_name = 'acceuil.html'


    def get_queryset(self):
        return service.objects.all()

    def get_context_data(self, **kwargs):

        context = super(Index,self).get_context_data(**kwargs)
        context['service_tt'] = service.objects.all()
        context['product_tt'] = Product.objects.all()
        return context




from oscar.apps.catalogue.models import *
from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView, ProductCategoryView as CoreProductCategoryView

class CatalogueView(CoreCatalogueView):
    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCategoryView(CoreProductCategoryView):
    def get_context_data(self, **kwargs):
        context = super(ProductCategoryView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def get_categories(self):
        """
        Return a product's categories or parent's if there is a parent product.
        """
        if self.is_child:
            return self.parent.categories
        else:
            return self.categories
    get_categories.short_description = ("Categories")

from django.views.generic import RedirectView, TemplateView
class HomeView(TemplateView):
    """
    This is the home page and will typically live at /
    """
    template_name = 'acceuil.html'

