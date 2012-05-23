import pymongo
from mongosearch.collector.models import CollectionMapping, CollectionContentType
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.datastructures import SortedDict
import json


class CreateMongoCollection( object ):
    
    request = ""
    
    def __init__( self , request=None ):
        self.request = request

    def upload_json( self, json_dump, unique_dict=None ):
        print "uploading"
        for key,value_list in json_dump.items():
            self.collection_name=key
            self.create_content( value_list )
            col_obj = CollectionMapping( key)
            load_all=True
            for value in value_list:
                if unique_dict:
                    res=col_obj.find_one(unique_dict)
                    if res:
                        col_obj.objects.update(unique_dict,value)
                        load_all=False
                if load_all:
                    col_obj.load_json( value )
        print "file uploaded"
        return HttpResponse( 'File Uploaded' )
        
    def create_db( self ):
        self.collection_name = self.request.POST['id_collection']
        file = self.request.FILES['id_json']
        f = file.read()
        json_dump = json.loads( str( f ) )
        self.create_content( json_dump )
        col_obj = CollectionMapping( self.collection_name )
        col_obj.load_json( json_dump )
        return HttpResponse( 'File Uploaded' )
    
    def upload_form( self ):
        return render_to_response( 'mongosearch/collector/uploaddata.html', locals(), context_instance = RequestContext( self.request ) )

    def create_content( self, json_dump ):
        json_list = list( json_dump )
        col_obj = CollectionContentType()
        if not  col_obj.find_one( { "collection_name":self.collection_name} ):
            col_obj.load_json( { "collection_name":self.collection_name, "key_names":{}, "user": ''} )

        data_obj = col_obj.find_one( { "collection_name":self.collection_name} )
        user = data_obj['user']
        previous_keys = data_obj['key_names']
        if not previous_keys:previous_keys=SortedDict()
        pre_keys = previous_keys.keys()

        keys_dict = SortedDict()
        for each in json_list:
            for i,key in enumerate(each.keys()):
                if key == 'user':
                    user = each[key]
                elif key not in keys_dict.keys():
                    keys_dict[key] = i

        for new_key in keys_dict.keys():
            if new_key in pre_keys:
                count = int( previous_keys[new_key] ) + int( keys_dict[new_key] )
                previous_keys[new_key] = count
            else:
                previous_keys[new_key] = keys_dict[new_key]
        row_data = col_obj.find_one( { "collection_name":self.collection_name} )
        row_data['key_names'] = previous_keys
        row_data['user'] = user

        col_obj.update( { "collection_name":self.collection_name} , {"$set":{'key_names':previous_keys, 'user': user}} )

    @classmethod
    def update_db(self,json_dump):
        for key,value_dict in json_dump.items():
                obj=CollectionMapping(key)
                obj.objects.update(value_dict['where'],value_dict['set'])

