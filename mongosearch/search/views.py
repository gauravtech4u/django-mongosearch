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
from forms import ConstraintForm, SearchForm
from mongosearch.collector.models import CollectionMapping, CollectionContentType
from bson.objectid import ObjectId

# add models to be displayed for search
ALLOWED_MODELS={
        'sampleset':{'search_fields':[('group__name','group')],'display_fields':[('name','name')]},
        'checklist':{'search_fields':[('name','name'),('group__name','group')],'display_fields':[('name','name')]},
        'company':{'search_fields':[('name','name'),('company_type','company type')],'display_fields':[('name','name'),('office_phone','office phone')]},
        }

class Data(object):
    pass

class AppSearch(object):    
    """ Provides Basic Functions for app search """    
    
    def get_app_models(self):
        """ gets list of apps present in your content type """
        ct_list=[]
        for collection in CollectionContentType().find({}):
            ct_list.append((collection['_id'],collection['collection_name']))
        return ct_list
    
    def get_model_fields(self):
        """ gets fields inside a particular model """
        
        model_id,field_list = self.request.GET.get('id'), []
        if model_id:
            field_list=self.get_model_meta(model_id)
        return json.dumps(field_list, separators=(',',':'))
    
    def add_constraint_formset(self):
        """ add constraint formset """
        model_id,field_list = self.request.GET.get('id'), []
        if model_id:
            field_list=self.get_model_meta(model_id)
        ConstraintFormSet = formset_factory(ConstraintForm)
        formset= ConstraintFormSet(prefix="searchform")
        for form in formset:
            form.fields['filters'].choices=map(lambda x:(x[0],x[1]), field_list)
        return formset
    
    def build_query(self):
        """ prepares query for searching """
        collection_id = self.request.POST.get('models')
        ct_obj=CollectionContentType()
        collection_name=ct_obj.find_one({'_id':ObjectId(collection_id)})['collection_name']
        collection_obj=CollectionMapping(collection_name)
        self.data_list=[]
        for key,value in self.constraint_dict.items():
            for data in collection_obj.find({key:value}):
                self.data_list.append(data)
            
    def add_contraint(self):
        """ gets additional constraint AND/OR """
        constraint_count=self.request.POST.get('searchform-TOTAL_FORMS')
        search_term=self.request.POST.get('term')
        filters=self.request.POST.get('filters')
        self.constraint_dict={'$and':[{filters:search_term}],}
        for i in range(0,int(constraint_count)):
            constraint=self.request.POST.get('searchform-'+str(i)+'-contraint')
            term=self.request.POST.get('searchform-'+str(i)+'-term')
            filters=self.request.POST.get('searchform-'+str(i)+'-filters')
            if self.constraint_dict.get(constraint):
                self.constraint_dict[constraint].append({filters:term})
            else:
                self.constraint_dict[constraint]=[{filters:term}]
        self.build_query()
    
    def build_data(self,model_id):
        self.field_list=map(lambda x:x[0],self.get_model_meta(model_id,'display_fields'))
        self.generic_list=[]
        for data in self.data_list:
            temp_list=[]
            for field in self.field_list:

                    temp_list.append(data.get(field))
            self.generic_list.append(temp_list)             
       
    @staticmethod         
    def get_model_all_fields( model_id ):
        
        content_type = ContentType.objects.get( id = model_id )
        model_obj = get_model( content_type.app_label, content_type.model )
        model_fields = model_obj._meta.fields
        return model_fields

    @staticmethod
    def get_model_meta( model_id,field_type='search_fields' ):
        """ takes model id as param and returns list of fileds """
        collection_obj=CollectionContentType()
        model_fields=[]
        for key,value in collection_obj.find_one({'_id':ObjectId(model_id)})['keys_name'].items():
            model_fields.append([key,key])
        return model_fields
        
    
class ModelListing(TemplateView,AppSearch):
    
    template_name="search/search.html"
    
    def get_context_data(self,**kwargs):
        self.form=SearchForm(self.get_app_models())
        return {'form':self.form}
        
    def post(self, request, *args, **kwargs):
        self.add_contraint()
        self.build_data(self.request.POST.get('models'))
        self.get_context_data()
        return render(self.request, self.template_name, self.__dict__)

class AjaxFillFields(TemplateView,AppSearch):

    def render_to_response(self, context, **response_kwargs):
        json_data=self.get_model_fields()
        return HttpResponse(json_data,'application/json')
        
class AjaxConstraint(TemplateView,AppSearch):

    template_name="search/constraint.html"
    
    def get_context_data(self,**kwargs):
        formset=self.add_constraint_formset()
        return {'formset':formset }