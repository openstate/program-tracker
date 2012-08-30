from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from topic.models import Selection, Topic
from django.utils import simplejson

# Create your views here.

def addLabel(request):
    if request.is_ajax() and request.method == 'POST':
        label = request.POST['label']
        maybeT = Topic.objects.filter(name=label)
        
        if maybeT:
            t = maybeT.get()
        else:
            t = Topic.objects.create(name = label)
        
        s = Selection.objects.create(
             paragraph_id = request.POST['pid'],
             startLetter = request.POST['start'],
             endLetter = request.POST['end'],
             user = request.user,
             topic = t,)
        
        if request.user.is_authenticated():
            result = {"start":s.startLetter, "end": s.endLetter, 'label': label, 'id': s.id}
        else:
        	result = {}
        
        
        message = simplejson.dumps(result)
        mimetype = 'application/json'
    else:
        message = "No XHR"
        mimetype = 'text/html'
    return HttpResponse(message, mimetype)