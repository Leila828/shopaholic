from django.conf.urls import include, url  # < Django-2.0
# from django.urls import include, path  # > Django-2.0
from django.contrib import admin
from oscar.app import application
from django.conf import settings
from django.conf.urls import url
from django.urls import path,include

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
<<<<<<< HEAD
from cashondelivery.dashboard.app import application as cod_app
=======

>>>>>>> d4078a1c350d5d663218bd294360be25f29db914


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', admin.site.urls),

<<<<<<< HEAD
    url(r'', application.urls),
    url(r'^boutique/', include('form.urls')),
    url(r'^dashboard/cod/', cod_app.urls),
    url(r'^dashboard/service/', include('apps.dashboard.Service.urls')),
    url(r'^dashboard/service/reviews/', include('apps.dashboard.Avis.urls')),
    # About static resource
    url(r'^about/', include('apps.about.urls')),
    url(r'^service/', include('apps.service.urls')),
    url(r'^acceuil/', include('acceuil.urls')),

=======

    url(r'', application.urls),
    url(r'^boutique/', include('form.urls')),

    url(r'^dashboard/service/', include('apps.dashboard.Service.urls')),

    # About static resource
    url(r'^about/', include('apps.about.urls')),
    url(r'^service/', include('apps.service.urls')),
>>>>>>> d4078a1c350d5d663218bd294360be25f29db914
  #  url(r'^service/reviews/', include('apps.avis.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)