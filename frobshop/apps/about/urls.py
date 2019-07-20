from django.conf.urls import url
from django.views.generic import TemplateView
<<<<<<< HEAD
app_name = 'about'
urlpatterns = [

    url(r'^about_us/$', TemplateView.as_view(template_name='about/about_us.html'), name = "about_us"),
    url(r'^privacy_policy/$', TemplateView.as_view(template_name='about/privacy_policy.html'), name = "privacy_policy"),
    url(r'^shopping_policy/$', TemplateView.as_view(template_name='about/shopping_policy.html'), name = "shopping_policy")
=======

urlpatterns = [

    url(r'^about_us/$', TemplateView.as_view(template_name='about/about_us.html')),
    url(r'^terms_of_service/$', TemplateView.as_view(template_name='about/terms_of_service.html')),
    url(r'^privacy_policy/$', TemplateView.as_view(template_name='about/privacy_policy.html')),
    url(r'^shopping_policy/$', TemplateView.as_view(template_name='about/shopping_policy.html'))
>>>>>>> d4078a1c350d5d663218bd294360be25f29db914
]