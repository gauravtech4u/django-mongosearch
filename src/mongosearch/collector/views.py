from mongosearch.collector.mongodb import CreateMongoCollection
import pymongo
from mongosearch.collector.models import CollectionMapping, CollectionContentType
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import json

def  upload_form( request ):
    obj = CreateMongoCollection( request ).upload_form()
    return obj

def  upload_json( request ):
    obj = CreateMongoCollection( request ).upload_json()
    return obj

def  create_db( request ):
    obj = CreateMongoCollection( request ).create_db()
    return obj

def  update_db( request ):
    obj = CreateMongoCollection( request ).update_db()
    return obj
