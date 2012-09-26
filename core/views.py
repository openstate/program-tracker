from django.template import Context, loader
from core.models import Party
from core.models import Section, SectionType
from core.models import Paragraph
from core.models import Program
from topic.models import Topic, Selection
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
import json
from string import split, translate, maketrans, lower
from django.utils import simplejson
from collections import defaultdict



def upload_program(request):
	json_data=open('/home/hiram/program-tracker/data.json')
	data = simplejson.load(json_data)
	json_data.close()
	
	s = Section.objects.create(name=data['head'])
	
	if "body" in data:
		 for p in data['body']:
			 s.paragraphs.create(text=p)
	
	si = 1
	if "sub" in data:
		 for subdata in data['sub']:
			  addsection(s, subdata, si)
			  si = si + 1
	
	s.save();
	return render_to_response('core/program.html')

		 
def addsection(section, data, si):
	if "type" in data:
		type= SectionType.objects.get(name=data['type'])
	else:
		type = SectionType.objects.get(name="tekst")

	s = Section(name=data['head'], type=type, order=si)
	s.save()
	
	i = 1
	if "body" in data:
		 for p in data['body']:
			 Paragraph(text=p, section_id=s.id, order=i).save()
			 i = i + 1
		 
	si = 1
	if "sub" in data:	
		 for subdata in data['sub']:
			  addsection(s, subdata, si)
			  si = si + 1
			  
	section.subsections.add(s)
	
