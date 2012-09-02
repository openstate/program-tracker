from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView

from core.models import Program


urlpatterns = patterns('core.views',
    # Examples:
    # url(r'^$', 'verkiezingen.views.home', name='home'),
    # url(r'^verkiezingen/', include('verkiezingen.foo.urls')),

    url(r'^$', ListView.as_view(
            queryset=Program.objects.all().order_by('-party'),
            template_name='core/index.html')),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(
            model=Program,
            template_name='core/program.html'),
            name='program_view'),
    url(r'^add/$', 'upload_program'),
    url(r'^words/$', 'words'),

)