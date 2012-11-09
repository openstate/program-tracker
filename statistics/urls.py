from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView, simple



urlpatterns = patterns('statistics.views',
    # Examples:
    # url(r'^$', 'verkiezingen.views.home', name='home'),
    # url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

    url(r'^$', 'index'),
    url(r'^calc/$', 'calc'),
    url(r'^year/(?P<pk>\d+)/$', 'year'),
    url(r'^party/(?P<pk>\d+)/$', 'party'),
    url(r'^topic/(?P<pk>\d+)/$', 'topic'),
)