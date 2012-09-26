from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('lda.views',
	# Examples:
	# url(r'^$', 'verkiezingen.views.home', name='home'),
	# url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

	url(r'^words/$', 'words'),
	url(r'^topics/$', 'topics'),
	url(r'^addTopics/$', 'addSelections'),
	url(r'^clear/$', 'clear'),

)