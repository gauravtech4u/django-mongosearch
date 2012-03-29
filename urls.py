from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^admin/', include(admin.site.urls)),                   
    
    url(r'^report/', include("mongosearch.collector.urls")),
    
    url(r'^search/', include("mongosearch.search.urls")),
)
