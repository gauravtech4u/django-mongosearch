from django.conf.urls.defaults import patterns , url
from views import *

urlpatterns = patterns( '',
        
         url( r'^$', ModelListing.as_view() , name = 'upload_form' ),
         
         url( r'^filters/$', AjaxFillFields.as_view() , name = 'appfilter' ),
         
         url( r'^constraint/$', AjaxConstraint.as_view() , name = 'appconstraint' ),
         
 )
