from django.conf.urls.defaults import patterns , url
<<<<<<< HEAD
from views import *

urlpatterns = patterns( '',
        
         url( r'^$', ModelListing.as_view() , name = 'upload_form' ),
         
         url( r'^filters/$', AjaxFillFields.as_view() , name = 'appfilter' ),
         
         url( r'^constraint/$', AjaxConstraint.as_view() , name = 'appconstraint' ),
         

        
         #url( r'^$', 'criteria' , name = 'criteria' ),
         
         url( r'^get-keys/$', 'get_keys' , name = 'get_keys' ),
         
         url( r'^filter-results/$', 'filter_results' , name = 'filter_results' ),

 )
