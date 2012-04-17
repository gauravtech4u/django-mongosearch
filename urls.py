from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns( '',

    url( r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT } ),

    url(r'^$', TemplateView.as_view(template_name='home.html')),

    url( r'^', include( 'mongosearch.collector.urls' ) ),
     
    url( r'^search/', include( 'mongosearch.search.urls' ) ),

    url( r'^account/', include( 'auth.urls' ) ),

 )

