# -*- coding: utf-8 -*-
from django.template import Context, loader
from core.models import Party
from core.models import Section, SectionType
from core.models import Paragraph
from core.models import Program
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
import json
import re
from string import split, translate, maketrans, lower
from django.utils import simplejson
from collections import defaultdict



# Create your views here.
def index(request):
    parties = Program.objects.all().order_by('-party')[:5]
    c = {
        'parties': parties,
    }
    return render_to_response('core/index.html', c)


def program(request, program_id):    
    program = get_object_or_404(Program, pk=program_id)

    c = {
        'program': program,
    }
    return render_to_response('core/program.html', c)


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
    
def words(request):
    common = set(x.strip().lower() for x in open('/home/hiram/program-tracker/top1000nl.txt'))
    wordlist = []
    ttable = dict.fromkeys(map(ord, ',.;:()‘"\'!@#$')+[0x201c, 0x201d, 0x2018, 0x2019], None)
    result = []

    for p in Paragraph.objects.all():
        presult = defaultdict(int)
        words = split(p.text.translate(ttable).lower())
        
        for word in words:
            if word in common:
               continue
        	
            wordlist, index = getwordIndex(wordlist, word)
            presult[index] += 1 
            
        result.append({"number": len(presult), "pcounts": presult.items})
        	
    return render_to_response('core/words.html', {"words": wordlist, "counts": result})

def getwordIndex(dict, word):
    if not word in dict:
       index = len(dict)
       dict.append(word)
       return dict, index
    else:
        return dict, dict.index(word)
