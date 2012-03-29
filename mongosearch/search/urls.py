from django.conf.urls.defaults import patterns , url

urlpatterns = patterns( 'mongosearch.search.views',
        
         url( r'^$', 'criteria' , name = 'criteria' ),
         
         url( r'^get-keys/$', 'get_keys' , name = 'get_keys' ),
         
         url( r'^filter-results/$', 'filter_results' , name = 'filter_results' ),
 )
