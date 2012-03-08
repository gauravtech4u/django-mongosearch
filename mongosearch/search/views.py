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
            print collection
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
        content_type = ContentType.objects.get( id = self.request.POST.get('models') )
        model_obj = get_model( content_type.app_label, content_type.model )
        query=self.constraint_dict.popitem()
        query=Q(**{query[1][1]+'__icontains':query[0]})
        for key,value in self.constraint_dict.items():
            if value[0] == '|':
                query|=Q(**{value[1]+'__icontains':key})
            else:
                query&=Q(**{value[1]+'__icontains':key})
        self.data_list=model_obj.objects.filter(query)            
            
    def add_contraint(self):
        """ gets additional constraint AND/OR """
        constraint_count=self.request.POST.get('searchform-TOTAL_FORMS')
        search_term=self.request.POST.get('term')
        filters=self.request.POST.get('filters')
        self.constraint_dict={search_term:['&',filters]}
        for i in range(0,int(constraint_count)):
            constraint=self.request.POST.get('searchform-'+str(i)+'-contraint')
            term=self.request.POST.get('searchform-'+str(i)+'-term')
            filters=self.request.POST.get('searchform-'+str(i)+'-filters')
            self.constraint_dict.update({term:[constraint,filters]})
        self.build_query()
    
    def build_data(self,model_id):
        self.field_list=self.get_model_meta(model_id,'display_fields')
        self.data_list=self.data_list.values_list(*map(lambda x:x[0],self.field_list))
       
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
        for key,value in collection_obj.find_one({'_id':ObjectId(model_id)})['key_names']:
            model_field.append([key,key])
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

    template_name="appsearch/constraint.html"
    
    def get_context_data(self,**kwargs):
        formset=self.add_constraint_formset()
        return {'formset':formset }