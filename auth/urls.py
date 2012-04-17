from django.conf.urls.defaults import url, patterns, include

from views import register, login, update_create_user
from django.contrib.auth import views as auth_views
urlpatterns = patterns('',
#    url(r'^register/$', register, name='register'),
    url(r'^login/$', login, {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
            {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^update_user/$', update_create_user)
)