from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import login, logout

from core.models import Program

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'verkiezingen.views.home', name='home'),
    # url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

	url(r'^$', ListView.as_view(
		queryset=Program.objects.all().order_by('-party'),
		template_name='core/index.html')),
    
    url(r'^program/', include('core.urls')),
    url(r'^topic/', include('topic.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
)

urlpatterns += staticfiles_urlpatterns()