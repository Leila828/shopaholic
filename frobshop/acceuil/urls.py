from django.urls import path,include
from django.conf.urls import url
from acceuil import views
from .views import *

app_name = 'acceuil'
urlpatterns = [
   path('', Index.as_view(),name='index'),



    ]
