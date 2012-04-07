import urlparse

from django.conf import settings
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login

from forms import RegistrationForm
from models import User as MongoUser

def _update_user(new_user, **kwargs):
    """
    method to update user data after registration
    """
    new_user.first_name = kwargs.get('first_name')
    new_user.last_name = kwargs.get('last_name')
    new_user.is_staff = kwargs.get('is_staff', False)
    new_user.is_active = kwargs.get('is_active', True)
    new_user.is_superuser = kwargs.get('is_superuser', False)
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