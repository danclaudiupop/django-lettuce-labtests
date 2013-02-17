from django.views.generic.simple import direct_to_template
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', direct_to_template, { 'template': 'index.html' },),
)
