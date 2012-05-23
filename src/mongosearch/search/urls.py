from django.conf.urls.defaults import patterns , url
from views import *

urlpatterns = patterns( '',
        
         url( r'^$', ModelListing.as_view() , name = 'mongo_search_form' ),
         
         url( r'^filters/$', AjaxFillFields.as_view() , name = 'appfilter' ),
         
         url( r'^constraint/$', AjaxConstraint.as_view() , name = 'appconstraint' ),
        
         #url( r'^$', 'criteria' , name = 'criteria' ),
         
         url( r'^get-keys/$', 'get_keys' , name = 'get_keys' ),
         
         url( r'^filter-results/$', 'filter_results' , name = 'filter_results' ),
         
         url( r'^edit-record/(?P<model_name>[-\S]+)/(?P<id>[-\S]+)/$', EditRecord.as_view() , name = 'edit_record' ),

 )
