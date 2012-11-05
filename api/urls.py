from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView

from topic.models import Selection, Topic

urlpatterns = patterns('api.views',
	# Examples:
	# url(r'^$', 'verkiezingen.views.home', name='home'),
	# url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

	#url(r'^getTopics/$', 'getTopics')
	url(r'^$', 'home'),
	url(r'^parties/$', 'parties'),
	url(r'^programs/$', 'programs'),
)
