from django.urls import path,include
from django.conf.urls import url
from .views import *


from django.contrib.auth.decorators import login_required

app_name = 'service'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', ServiceView.as_view(), name='detail'),
    path('categories/', CategoriesView.as_view(), name='categories-list'),
    path('categories/<int:pk>/', CategoryView.as_view(), name='service_list_category'),
    path('<int:pk>/reviews/', include('apps.avis.urls')),

]