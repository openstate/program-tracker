from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, simple

from topic.models import Source



urlpatterns = patterns('statistics.views',
    # Examples:
    # url(r'^$', 'verkiezingen.views.home', name='home'),
    # url(r'^verkiezingen/', include('verkiezingen.foo.urls')),
    
    url(r'^$', ListView.as_view(model=Source)),
    url(r'^(?P<source>\w+)/$', 'sourceindex'),
    url(r'^(?P<source>\w+)/calc/$', 'calc'),
    url(r'^(?P<source>\w+)/year/(?P<pk>\d+)/$', 'year'),
    url(r'^(?P<source>\w+)/party/(?P<pk>\d+)/$', 'party'),
    url(r'^(?P<source>\w+)/topic/(?P<pk>\d+)/$', 'topic'),
)