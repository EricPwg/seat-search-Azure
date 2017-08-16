"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url
from django.views.static import serve
import django.contrib.auth.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

from restaurant.views import *

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
#                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^(\d{1,2})/plus/(\d{1,2})$', app.views.add),
    url(r'^api/messages$', app.views.messages),
    url(r'^restaurant$', restaurant),
#    url(r'^restaurant$', app.views.restaurant),
    url(r'^image$', app.views.image),
    url(r'^LED$', led),
    url(r'^personal$', personal),
    url(r'^seat$', seat),

    url(r'^([a-z,A-Z,0-9]*)/seatreserve/(\d{1,3})$', seat_reserve),
    url(r'^([a-z,A-Z,0-9]*)/seatunlock/(\d{1,3})$', seat_unlock),
    url(r'^([a-z,A-Z,0-9]*)/restaurantreserve/([0-9]*)$', restaurant_reserve),
    url(r'^([a-z,A-Z,0-9]*)/restaurantcheckin/([0-9]*)$', restaurant_check_in),

    url(r'^seat_old$', app.views.seat),

    #url(r'^media/(?P<path>.*)$', serve, {'document_root': '/static/media'}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': '/home/site/wwwroot/app/static/images'}),

    url(r'^static/(?P<path>.*)$', serve, {'document_root': '/home/site/wwwroot/static'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^[^/]*/test', app.views.draw, name='test'),
]
#print type(urlpatterns)
#print type(staticfiles_urlpatterns)

#urlpatterns.extend([staticfiles_urlpatterns])
#urlpatterns = urlpatterns+staticfiles_urlpatterns