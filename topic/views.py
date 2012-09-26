from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from topic.models import Selection, Topic, Source
from django.utils import simplejson

# Create your views here.

def addLabel(request):
	if request.is_ajax() and request.method == 'POST':
		label = request.POST['label']

		if request.user.is_authenticated():
			user = request.user
		else:
			user = None
		source, created = Source.objects.get_or_create(name = 'user')

		t, created = Topic.objects.get_or_create(name = label, source = source)
		
		s = Selection.objects.create(
			paragraph_id = request.POST['pid'],
			startLetter = request.POST['start'],
			endLetter = request.POST['end'],
			source = source,
			user = user,
			topic = t,)
		
		if request.user.is_authenticated():
			result = {"start":s.startLetter, "end": s.endLetter, 'label': label, 'id': s.id, 'source_color':s.source.color, 'topic_name': t.name, 'topic_id': t.id, 'topic_desc': t.description}
		else:
			result = {"start":s.startLetter, "end": s.endLetter, 'label': label, 'id': s.id, 'source_color':s.source.color, 'topic_name': t.name, 'topic_id': t.id, 'topic_desc': t.description}
		
		
		message = simplejson.dumps(result)
		mimetype = 'application/json'
	else:
		message = "No XHR"
		mimetype = 'text/html'
	return HttpResponse(message, mimetype)


def getTopics(request):
	if request.is_ajax():
		term = request.GET.get('term', '')
		topics = list(Topic.objects.filter(name__istartswith=term).order_by('name').values_list('name', flat=True))
		
		message = simplejson.dumps(topics)
		mimetype = 'application/json'
	else:
		message = "No XHR"
		mimetype = 'text/html'
	return HttpResponse(message, mimetype)	