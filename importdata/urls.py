from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView

from importdata.models import Partij


urlpatterns = patterns('importdata.views',
	# Examples:
	# url(r'^$', 'verkiezingen.views.home', name='home'),
	# url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

	url(r'^$', ListView.as_view(
			queryset=Partij.objects.all().order_by('-partij'))),
	url(r'^(?P<pk>\d+)/$', 'partij'),
	url(r'^add/(?P<file>\w+)/to/(?P<program_id>\d+)/$', 'upload_program'),
)