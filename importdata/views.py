import re 
import json
from string import split, translate, maketrans, lower
from collections import defaultdict
from xml.dom.minidom import parse

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson
from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.conf import settings

from core.models import Party
from core.models import Section, SectionType
from core.models import Paragraph
from core.models import Program
from topic.models import Topic, Selection, Source
from importdata.models import Partij


def partij(request, pk):
    '''
        This is the most ugly method you will ever find, but since it is only for importing don't hold it against me :-)
        Part of the reformatting is done in the template and using a custom filter
    '''
    data = Partij.objects.get(pk = pk)
    content = render_to_response('importdata/partij_detail.html', {"partij": data}, mimetype="text/plain").content
    content = simplejson.loads(content)
    string = simplejson.dumps(content)
    string = re.sub(r', {}', r'', string, flags=re.S )
    string = re.sub(r', "sub": \[\]', r'', string, flags=re.S )
    string = re.sub(r'"head": "[\d\.\sIXV]+( |\.)', r'"head": "', string, flags=re.S ) #Strip numbers from head
    #string = re.sub(r'"sub": \[{"head": "", "sub": \[{"body": \[(.+?)\]}\]}\]', r'"body": [\1]', string, flags=re.S )
        
    content = simplejson.loads(string)
    
    rreduce(content)
    
    string = simplejson.dumps(content, indent=True, sort_keys=True)
    string = re.sub(r'\n\s+"",[ ]*', r'', string, flags=re.S )

    return HttpResponse(string, mimetype='text/plain')
    
    
    
def rreduce(node):

    if 'sub' in node:
        for sub in node['sub']:
            rreduce(sub)
    
        sub = node['sub'][0]
        if not 'body' in node and len(node['sub']) == 1 and (not 'head' in sub or sub['head'].strip() == ''):
            if 'sub' in sub:
                node['sub'] = sub['sub']
            else:
                del node['sub']
            if 'body' in sub:
                node['body'] = sub['body']
        elif not 'body' in node and (not 'head' in sub or sub['head'].strip() == ''):
            if 'sub' in sub:
                sub['sub'].extend(node['sub'][1:])
                node['sub'] = sub['sub']
            else:
                del node['sub']
            if 'body' in sub:
                node['body'] = sub['body']
        
                
            

def upload_program(request, file, program_id):
    #delete old sections and paragraphs
    program = Program.objects.get(pk=program_id)
    Section.objects.filter(program__isnull=True).delete()
    Section.objects.filter(program = program).delete()



    json_data=open(settings.PROJECT_DIR("programmas") + '/%s.json' % file)
    data = simplejson.load(json_data)
    json_data.close()
    
    s = Section.objects.create(name=data['head'], program=program)
    program.section = s
    program.save()
    
    if "body" in data:
         for p in data['body']:
             s.paragraphs.create(text=p)
    
    si = 1
    if "sub" in data:
         for subdata in data['sub']:
              addsection(s, subdata, si, program)
              si = si + 1
    
    s.save();
    return render_to_response('core/program.html')

         
def addsection(section, data, si, program):
    if "type" in data:
        type= SectionType.objects.get(name=data['type'])
    else:
        type = SectionType.objects.get(name="tekst")

    s = Section(name=data['head'], type=type, order=si, program=program)
    s.save()
    
    i = 1
    if "body" in data:
         for p in data['body']:
             Paragraph(text=p, section_id=s.id, order=i).save()
             i = i + 1
         
    si = 1
    if "sub" in data:    
         for subdata in data['sub']:
              addsection(s, subdata, si, program)
              si = si + 1
              
    section.subsections.add(s)
    
def upload_lipschits(request, year):
    #delete old
    Program.objects.filter(date = '%s-01-01' % year).delete()
    Section.objects.filter(program__date = '%s-01-01' % year).delete()

    xml = parse(settings.PROJECT_DIR("LipschitsBooksinXML") + '/VP_%s.party-topicnr-content.xml' % year)
    chapters = xml.getElementsByTagName("chapter")
    for chapter in chapters:        
        pm_id = chapter.getAttributeNode('party').value
        party, created = Party.objects.get_or_create(pm_id=pm_id, defaults={"full_name": pm_id, "name": pm_id})
        program = Program(party=party, name = "Programma %s" % year, date = ('%s-01-01' % year))
        type = SectionType.objects.get(name="tekst")
        program.save()
        s = Section.objects.create(name = "Programma %s" % year, type=type, order=1, program=program)
        program.section = s
        program.save()
        
        for p in chapter.getElementsByTagName("p"):
            text = " ".join(t.nodeValue for t in p.childNodes if t.nodeType == t.TEXT_NODE)
            text = process_text(text)
            paragraph = s.paragraphs.create(text=text)
            
            for theme in p.getElementsByTagName('theme'):
                name = theme.getAttributeNode('id').value

                source, created = Source.objects.get_or_create(name = 'lipschits')

                t, created = Topic.objects.get_or_create(
                    name = name,
                    source = source)
            
                Selection.objects.create(
                    source = source,
                    paragraph = paragraph,
                    startLetter = 0,
                    endLetter = -1,
                    user = None,
                    topic = t,)
     
    return render_to_response('core/program.html')
    
def process_text(text):
    text = re.sub(r'\d+', '', text)