<<<<<<< HEAD
import django_filters
from .models import *


class ServiceFilters(django_filters.FilterSet):
   wilaya = django_filters.ChoiceFilter(choices=service.wilay)

   class Meta:
        Model = service
        fields = ['wilaya']
=======
>>>>>>> d4078a1c350d5d663218bd294360be25f29db914

