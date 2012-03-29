from mongosearch.collector.models import CollectionMapping, CollectionWrapper
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from choices import SEARCH_SET, CURSOR_FUNC

class MongoSearch( object ):
    
    request = ""
    
    def __init__( self , request ):
        self.request = request 
        
    def criteria( self ):        
        collections_name = CollectionWrapper.collection_names()
        return render_to_response( 'search/criteria.html', locals(), context_instance = RequestContext( self.request ) )

    def get_keys( self ):
        collection_name = self.request.GET['collection_name']
        col_obj = CollectionMapping( 'mongo_content' )
        data_obj = col_obj.find_one( { "collection_name":collection_name} )
        keys_name = ( data_obj['key_names'] ).keys()
        search_set = list( SEARCH_SET )
        return render_to_response( 'search/key_list.html', locals(), context_instance = RequestContext( self.request ) )

    def filter_results( self ):
        post_dict = self.request.POST
        post_dict._mutable = True
        
        import pdb;pdb.set_trace()
        pass
