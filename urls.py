from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns( '',

     url( r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT } ),

     url( r'^', include( 'mongosearch.collector.urls' ) ),
     
     url( r'^search/', include( 'mongosearch.search.urls' ) ),

 )

