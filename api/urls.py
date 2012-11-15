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
	url(r'^programs/(?P<program_id>\d+)/$', 'program'),
	url(r'^programs/(?P<program_id>\d+)/sections/$', 'sections'),
	url(r'^programs/(?P<program_id>\d+)/selections/$', 'selections'),
	url(r'^section_types/$', 'section_types'),
	url(r'^sources/$', 'sources'),
	url(r'^topics/$', 'topics'),
	url(r'^paragraphs/(?P<paragraph_id>\d+)/$', 'paragraph'),
	url(r'^sections/(?P<section_id>\d+)/$', 'section')
)
