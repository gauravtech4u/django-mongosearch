import pymongo
from pymongo import Connection
import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import json
class CreateMongoCollection( object ):
    
    request = ""
    
    def __init__( self , request ):
        self.request = request 
        
    def create_db( self ):
        connection = Connection( settings.DB_CONNECTION , 27017 )
        db_name = self.request.POST['id_collection']
        db = connection[str( db_name )]
        file = self.request.FILES['id_json']
        f = file.read()
        json_dump = json.loads( str( f ) )
        db.__getattr__( db_name ).insert( json_dump )
        for post in  db.__getattr__( db_name ).find():
            print post
        return HttpResponse( 'True' )
    
    def upload_form( self ):
        
        
        return render_to_response( 'collector/uploaddata.html', locals(), context_instance = RequestContext( self.request ) )

    
