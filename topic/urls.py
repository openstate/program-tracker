from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView

from topic.models import Selection, Topic

urlpatterns = patterns('topic.views',
	# Examples:
	# url(r'^$', 'verkiezingen.views.home', name='home'),
	# url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

	url(r'^addLabel/$', 'addLabel'),
	url(r'^$', ListView.as_view(
			queryset=Topic.objects.all().order_by('-source', 'name'),
			template_name='topic/index.html')),
	url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Topic), name='topic_view'),
	url(r'^getTopics/$', 'getTopics')
)
