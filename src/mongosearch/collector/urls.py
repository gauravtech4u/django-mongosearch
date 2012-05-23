from django.conf.urls.defaults import patterns , url

urlpatterns = patterns( 'mongosearch.collector.views',
        
        url( r'^upload/$', 'upload_form' , name = 'upload_form' ),
         
        url( r'^upload_json/$', 'upload_json' , name = 'upload_json' ),

        url( r'^create/$', 'create_db' , name = 'create_db' ),

        url( r'^update/$', 'update_db' , name = 'update_db' ),

 )
