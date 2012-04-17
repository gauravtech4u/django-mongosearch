import urlparse, json

from django.conf import settings
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login


from forms import RegistrationForm
from models import User as MongoUser

def _update_user(new_user, **kwargs):
    """
    method to update user data after registration
    """
    for key, value in kwargs.items():
        if key not in ['username', 'password1', 'email', 'password', 'password2']:
            new_user.__setattr__(key, value)
    new_user.save()
    return new_user

def register(request, success_url=None, form_class=None,
             template_name='registration/registration_form.html',
             extra_context=None):

    if form_class is None:
        form_class = RegistrationForm

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_user = MongoUser.create_user(data['username'], data['password1'], data['email'])
            _update_user(new_user, **data)
            if success_url is None:
                success_url = settings.LOGIN_URL
                return redirect(success_url)
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
            {'form': form},
        context_instance=context)

@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
        context_instance=RequestContext(request, current_app=current_app))

class CreateUpdateUser(object):
    def __init__( self , request ):
        self.request = request

    def create_update_user(self):
        json_dict = self.request.POST.get('data')
        json_dump = json.loads( json_dict )

        username = json_dump.get('username')
        existing = MongoUser.objects(username=username)
        if existing:
            user = existing[0]
            for key, value in json_dump.items():
                user.__setattr__(key, value)
            user.save()
        else:
            user = MongoUser()
            for key, value in json_dump.items():
                user.__setattr__(key, value)
            user.save()
        return HttpResponse(True)


def update_create_user(request):
    return CreateUpdateUser(request).create_update_user()