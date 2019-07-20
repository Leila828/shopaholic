
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ungettext_lazy
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from oscar.core.loading import get_class, get_model
from oscar.apps.dashboard.tables import DashboardTable
from apps.service.models import service,category


class ServiceTable(DashboardTable):
    name = TemplateColumn(
        verbose_name=_('Nom'),
        template_name='dashboard/service/service_row_title.html',
        order_by='name', accessor=A('name'))
    image = TemplateColumn(
        verbose_name=_('Image'),
        template_name='dashboard/service/service_row_image.html',
        orderable=False)
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/service/service_row_actions.html',
        orderable=False)

    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = service
       # sequence = ('name', 'image', 'email', 'tel', 'actions')
        exclude = ['rating', 'description', 'id']


class CategoryTable(DashboardTable):
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/service/category_row_actions.html',
        orderable=False)
    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = category
        fields = ('name', 'description', 'image')