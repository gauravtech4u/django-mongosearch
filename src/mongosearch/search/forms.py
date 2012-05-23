from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets

ALLOWED_CONSTRAINTS=(
    ('','-----'),('$lt','<'),('$gt','>'),('$lte','<='),('$gte','>='),
)

class SearchForm( forms.Form ):
    """ initial form with models list for appsearch """
    models      =   forms.ChoiceField()
    constraint  =   forms.ChoiceField()
    filters     =   forms.ChoiceField(label="filter by",choices=[])
    term        =   forms.CharField(label="Search Term")
    
    def __init__(self, model_list, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        model_list.insert(0,('','Select'))
        self.fields['models'].choices = model_list
        self.fields['constraint'].choices = ALLOWED_CONSTRAINTS
        
    #class Meta:
    #    widgets = {'choice': forms.TextInput( attrs = {'class   ':'validate[required]'} ),}
    
class ConstraintForm(forms.Form):
    """ form adds up constraints along with initial form """   
    
    contraint       =   forms.ChoiceField(label="Add Constraint",choices=[('$or','OR'), ('$and','AND')])
    add_constraint  =   forms.ChoiceField(label="Additional Constraint",choices=ALLOWED_CONSTRAINTS)
    filters         =   forms.ChoiceField(label="filter by",choices=[])
    term            =   forms.CharField(label="Search Term") 

class EditForm(forms.Form):
    pass