from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from topic.models import Selection, Topic, Source
from django.utils import simplejson

def home(request):
    message = "No XHR"
    mimetype = 'text/html'
    return HttpResponse(message, mimetype)
    