
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