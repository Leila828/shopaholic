from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'Avis'
urlpatterns = [

  path('', ReviewListView.as_view(), name='reviews_list'),
  path('<int:pk>/delete/',ReviewDeleteView.as_view(), name='review_delete'),


]