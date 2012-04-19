from mongosearch.search.genericsearch import MongoSearch

from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import ContentType
from django.http import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.db.models import get_model
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q    
from django.utils import simplejson as json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from forms import ConstraintForm, SearchForm, EditForm
from mongosearch.collector.models import CollectionMapping, CollectionContentType
from bson.objectid import ObjectId

def  criteria( request ):
    obj = MongoSearch( request ).criteria()
    return obj

def  get_keys( request ):
    obj = MongoSearch( request ).get_keys()
    return obj

def filter_results( request ):
    obj = MongoSearch( request ).filter_results()
    return obj

# add models to be displayed for search
ALLOWED_MODELS = {
        'test':{'search_fields':[( 'group__name', 'group' )], 'display_fields':[( 'app_type', 'App Type' ),('amount','Amount'),('email','Email'),('registration_no','Registration Number')]},
        }

class Data( object ):
    pass

class AppSearch( object ):    
    """ Provides Basic Functions for app search """    
    
    def get_app_models( self ):
        """ gets list of apps present in your content type """
        ct_list = []
        for collection in CollectionContentType().find( {} ):
            ct_list.append( ( collection['_id'], collection['collection_name'] ) )
        return ct_list
    
    def get_model_fields( self ):
        """ gets fields inside a particular model """
        
        model_id, field_list = self.request.GET.get( 'id' ), []
        if model_id:
            model_name,field_list = self.get_model_meta( model_id )
        return json.dumps( field_list, separators = ( ',', ':' ) )
    
    def add_constraint_formset( self ):
        """ add constraint formset """
        model_id, field_list = self.request.GET.get( 'id' ), []
        if model_id:
            model_name,field_list = self.get_model_meta( model_id )
        ConstraintFormSet = formset_factory( ConstraintForm )
        formset = ConstraintFormSet( prefix = "searchform" )
        for form in formset:
            form.fields['filters'].choices = map( lambda x:( x[0], x[1] ), field_list )
        return formset
    
    def build_query( self ):
        """ prepares query for searching """

        collection_id = self.request.POST.get( 'models' )
        ct_obj = CollectionContentType()
        collection_name = ct_obj.find_one( {'_id':ObjectId( collection_id )} )['collection_name']
        collection_obj = CollectionMapping( collection_name )
        self.data_list = collection_obj.objects.filter(self.constraint_dict)

            
    def add_contraint( self ):
        """ gets additional constraint AND/OR """
        constraint_count = self.request.POST.get( 'searchform-TOTAL_FORMS' )
        search_term = self.request.POST.get( 'term' )
        filters = self.request.POST.get( 'filters' )
        if self.request.POST.get('constraint' ):
            search_term={self.request.POST.get('constraint' ):int(search_term)}
        self.constraint_dict = {'$or':[{filters:search_term}], }
        for i in range( 0, int( constraint_count ) ):
            constraint = self.request.POST.get( 'searchform-' + str( i ) + '-contraint' )
            term = self.request.POST.get( 'searchform-' + str( i ) + '-term' )
            filters = self.request.POST.get( 'searchform-' + str( i ) + '-filters' )
            if self.request.POST.get('searchform-' + str( i ) + '-add_constraint' ):
                term={self.request.POST.get('searchform-' + str( i ) + '-add_constraint' ):int(term)}
            if self.constraint_dict.get( constraint ):
                self.constraint_dict[constraint].append( {filters:term} )
            else:
                self.constraint_dict[constraint] = [{filters:term}]
        self.build_query()
    
    def get_display_fields(self,model_id=None):
        
        self.collection_name,field_list= self.get_model_meta( model_id, 'display_fields' )
        if ALLOWED_MODELS.get(self.collection_name):
            field_list=ALLOWED_MODELS[self.collection_name]['display_fields']
        return field_list
    
    def build_data( self, model_id ):
        self.field_list=self.get_display_fields(model_id)
        self.generic_list = []
        print self.data_list
        for data in self.data_list:
            temp_list = []
            for field,field_name in self.field_list:
                try:
                    temp_list.append( data.__getattribute__( field ) )
                except:pass
            self.generic_list.append( (data._id,temp_list) )
        self.display_fields=map(lambda x:x[1],self.field_list)
       
    @staticmethod         
    def get_model_all_fields( model_id ):
        content_type = ContentType.objects.get( id = model_id )
        model_obj = get_model( content_type.app_label, content_type.model )
        model_fields = model_obj._meta.fields
        return model_fields

    @staticmethod
    def get_model_meta( model_id, field_type = 'search_fields' ):
        """ takes model id as param and returns list of fields """

        collection_obj = CollectionContentType()
        model_fields = []
        col_data=collection_obj.find_one( {'_id':ObjectId( model_id )} )
        for key,value in col_data['key_names'].items():
            model_fields.append( [key,key] )
        return (col_data['collection_name'],model_fields)
        
    
class ModelListing( TemplateView, AppSearch ):
    
    template_name = "search/search.html"
    
    def get_context_data( self, **kwargs ):
        self.form = SearchForm( self.get_app_models() )
        return {'form':self.form}
        
    def post( self, request, *args, **kwargs ):
        self.add_contraint()
        self.build_data( self.request.POST.get( 'models' ) )
        self.get_context_data()
        return render( self.request, self.template_name, self.__dict__ )

class AjaxFillFields( TemplateView, AppSearch ):

    def render_to_response( self, context, **response_kwargs ):
        json_data = self.get_model_fields()
        return HttpResponse( json_data, 'application/json' )
        
class AjaxConstraint( TemplateView, AppSearch ):

    template_name = "search/constraint.html"
    
    def get_context_data( self, **kwargs ):
        formset = self.add_constraint_formset()
        return {'formset':formset }

class EditRecord(TemplateView,AppSearch):
    template_name = "search/edit_data.html"
    
    def get_context_data( self, **kwargs ):
        form=EditForm()
        collection_name=self.kwargs.get('model_name')
        collection_obj = CollectionMapping( collection_name )
        return {'form':form }  