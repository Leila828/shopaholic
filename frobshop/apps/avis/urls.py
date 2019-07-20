from django.urls import path
from django.conf.urls import url
from .views import *

from django.contrib.auth.decorators import login_required

app_name = 'avis'
urlpatterns = [
    path('create/', CreateServiceReview.as_view(), name='create'),
    path('<int:pk>/', ServiceReviewDetail.as_view(), name='detail'),
]