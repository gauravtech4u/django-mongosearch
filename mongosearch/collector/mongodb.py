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
        
        collection_name = self.request.POST['id_collection']
        file = self.request.FILES['id_json']
        db_name = settings.DB_CONNECTION
        db_col = db_name[collection_name]
        f = file.read()
        json_dump = json.loads( str( f ) )
        self.create_content( json_dump )
        db_col.insert( json_dump )
        for post in  db_col.find():
            print post
        return HttpResponse( 'True' )
    
    def upload_form( self ):
        return render_to_response( 'collector/uploaddata.html', locals(), context_instance = RequestContext( self.request ) )

    def create_content( self, json_dump ):
        db_name = settings.DB_CONNECTION
        json_list = list( json_dump )
        collection_name = self.request.POST['id_collection']
        db_col = db_name['mongo_content']
        if not  db_col.find( { "collection_name":collection_name} ):
            db_col.insert( { "collection_name":collection_name, "key_names":{}} )
        keys_dict = {}
        for each in json_list:
            for key in each.keys():
                if key not in keys_dict.keys():
                    keys_dict[key] = 1
                else:
                    keys_dict[key] = int( keys_dict[key] ) + 1 
        data_obj = db_col.find_one( { "collection_name":collection_name} )
        previous_keys = data_obj['key_names']
        pre_keys = previous_keys.keys()
        for new_key in keys_dict.keys():
            if ( new_key in pre_keys ):
                count = int( previous_keys[new_key] ) + int( keys_dict[new_key] )
                previous_keys[new_key] = count
            else:
                previous_keys[new_key] = keys_dict[new_key]
        row_data = db_col.find_one( { "collection_name":collection_name} )
        row_data['key_names'] = previous_keys
        db_col.save( row_data )
        return True
        
