from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django_tables2 import SingleTableView

from .forms import *
from apps.service.models import *
from .tables import *
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.utils import timezone




def category_create(request):
    if request.method == 'POST':
            form = CategoryFormCreate(request.POST)
            if form.is_valid():
                form.save()
                return  HttpResponseRedirect("/dashboard/service/category")

    return render(request, 'dashboard/service/category_create.html', {'categoryForm': CategoryFormCreate})



@login_required
def service_create(request):

    ImageFormSet = modelformset_factory(ServiceImage,
                                        form=ServiceImageForm, extra=3)

    if request.method == 'POST':

        postForm = ServiceForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=ServiceImage.objects.none())


        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.save()

            if 'image' in formset:
                  image = formset['image']
                  photo = ServiceImage(service=post_form, image=image)
                  photo.save()
            messages.success(request,
                             "Posted!")
            return HttpResponseRedirect("/dashboard")

    return render(request, 'dashboard/service/service_create.html',
                  {'postForm': ServiceForm, 'formset': ImageFormSet})


class IndexView(generic.ListView):
    template_name = 'dashboard/service/service_all.html'
    context_object_name = 'service_tt'

    def get_queryset(self):
        return service.objects.order_by('name')


class categoryListViews(SingleTableView):
    template_name = 'dashboard/service/category_all.html'
    table_class =  CategoryTable
    context_table_name = "category"

    def filter_queryset(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = category.objects.all()
        queryset = self.filter_queryset(queryset)
        return queryset

class ServiceListView(SingleTableView):

    template_name = 'dashboard/service/service_all.html'
    form_class = ServiceSearchForm
    table_class = ServiceTable
    context_table_name = 'services'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx

    def get_description(self, form):
        if form.is_valid() and any(form.cleaned_data.values()):
            return ('Service search results')
        return ('Services')

    def get_table(self, **kwargs):
        if 'recently_edited' in self.request.GET:
            kwargs.update(dict(orderable=False))

        table = super().get_table(**kwargs)
        table.caption = self.get_description(self.form)
        return table

    def get_table_pagination(self, table):
        return dict(per_page=20)

    def filter_queryset(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = service.objects.all()
        queryset = self.filter_queryset(queryset)
        queryset = self.apply_search(queryset)
        return queryset

    def apply_search(self, queryset):
        self.form = self.form_class(self.request.GET)

        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        if data.get('UPC'):
            matches_upc = service.objects.filter(UPC=data['UPC'])
            qs_match = queryset.filter(
                Q(id__in=matches_upc.values('id')))

            if qs_match.exists():
                queryset = qs_match
            else:
                matches_upc = service.objects.filter(upc__icontains=data['upc'])
                queryset = queryset.filter(
                    Q(id__in=matches_upc.values('id')) | Q(id__in=matches_upc.values('parent_id')))

        if data.get('name'):
            queryset = queryset.filter(title__icontains=data['name'])

        return queryset

class CategoryDeleteViews(generic.DeleteView):
    template_name = 'dashboard/service/category_delete.html'
    model = category
    context_object_name = 'category'

    def get_queryset(self):
        return category.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = ("Supprimer la categorie?")
        return ctx

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
            return reverse('Service:category_list')



class ServiceDeleteView(generic.DeleteView):

    template_name = 'dashboard/service/service_delete.html'
    model = service
    context_object_name = 'service'

    def get_queryset(self):
        return service.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = ("Supprimer le service ?")
        return ctx

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
            return reverse('Service:service_list')

