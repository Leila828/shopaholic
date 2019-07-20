from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'Service'
urlpatterns = [
  path('create/', service_create, name='service_create'),
  path('<int:pk>/', service_create, name='service_edit'),
  path('', ServiceListView.as_view(), name='service_list'),
  path('<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
  path('category/', categoryListViews.as_view(), name='category_list'),
  path('category/create', category_create, name='category_create'),
  path('category/<int:pk>/delete/',CategoryDeleteViews.as_view(),name='category_delete'),

]